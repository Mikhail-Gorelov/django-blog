import datetime
from urllib.parse import urljoin

from allauth.account.models import EmailAddress
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from dj_rest_auth.serializers import PasswordChangeSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.status import HTTP_400_BAD_REQUEST

from actions.models import Follower, Like
from blog.models import Article, Comment
from main.services import CeleryService, MainService
from user_profile import choices

from . import models
from .choices import GenderChoice
from .models import Profile
from .services import UserProfileService

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.URLField(source="avatar_url")

    class Meta:
        model = Profile
        fields = ["gender", "image", "birthdate", "bio", "website"]


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    subscribers = serializers.SerializerMethodField("get_subscribers_count")
    has_subscribed = serializers.SerializerMethodField("get_has_subscribed")

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.update(rep.pop("profile", {}))
        return rep

    def get_subscribers_count(self, obj):
        return obj.subscribers_count()["count"]

    def get_has_subscribed(self, obj):
        try:
            Follower.objects.get(
                subscriber=self.context["request"].user,
                to_user=User.objects.get(pk=obj.pk),
            )
            has_subscription = True
        except Follower.DoesNotExist:
            has_subscription = False

        return has_subscription

    class Meta:
        model = User
        fields = ["full_name", "id", "profile", "subscribers", "has_subscribed"]


class TrueUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep.update(rep.pop("profile", {}))
        return rep

    class Meta:
        model = User
        fields = ["full_name", "id", "profile"]


class ChangePasswordSerializer(PasswordChangeSerializer):
    old_password = serializers.CharField()
    new_password1 = serializers.CharField(min_length=8)
    new_password2 = serializers.CharField(min_length=8)


class ChangeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["image"]

    def validate(self, attrs):
        limit = 4 * 1024 * 1024  # 4 mb
        if attrs.get("image").size > limit:
            raise serializers.ValidationError(
                "File too large. Size should not exceed 4 MiB."
            )
        return attrs


class UserShortInfoSerializer(serializers.ModelSerializer):
    image = serializers.URLField(source="avatar_url")
    profile = serializers.URLField(source="get_absolute_url")

    class Meta:
        model = User
        fields = ("id", "full_name", "image", "profile")


class GetUsersIdSerializer(serializers.Serializer):
    user_id = serializers.ListField(child=serializers.IntegerField())

    def validate(self, attrs):
        users = set(
            models.User.objects.filter(pk__in=attrs["user_id"]).values_list(
                "id", flat=True
            )
        )
        not_existed_users = set(attrs["user_id"]).difference(users)
        errors = {user: "Not found" for user in not_existed_users}
        if errors:
            raise serializers.ValidationError(errors)
        return attrs


class ProfileUpdateSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(required=False, source="profile.birthdate")
    gender = serializers.ChoiceField(
        required=False, choices=choices.GenderChoice.choices, source="profile.gender"
    )
    email = serializers.EmailField()
    website = serializers.URLField(source="profile.website")
    biography = serializers.CharField(source="profile.bio")

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "birthday",
            "gender",
            "website",
            "biography",
        ]

    def save(self, **kwargs):
        user = User.objects.get(id=kwargs.get("id"))
        data = self.validated_data.copy()
        profile_data = data.pop("profile")
        user_data = dict(data)
        User.objects.filter(id=kwargs.get("id")).update(**user_data)
        models.Profile.objects.filter(user__pk=kwargs.get("id")).update(**profile_data)
        email = EmailAddress.objects.get(user__pk=kwargs.get("id"))
        UserProfileService.deactivate_email(email)
        EmailAddress.objects.filter(user__pk=kwargs.get("id")).update(
            email=user_data["email"]
        )
        CeleryService.send_email_confirm(user)


class NewsFeedArticleShortSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField("get_slug")

    def get_slug(self, obj):
        backend_site = urljoin(settings.BACKEND_SITE, "/")
        posts = urljoin(backend_site, "posts/")
        article = urljoin(posts, obj.slug) + "/"
        return article

    class Meta:
        model = Article
        fields = ["title", "slug"]


class NewsFeedArticleSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField("get_author")
    updated = serializers.SerializerMethodField("get_updated")
    type = serializers.SerializerMethodField("get_type")

    def get_author(self, obj):
        author = obj.author
        serializer = UserShortInfoSerializer(author)
        return serializer.data

    def get_updated(self, obj):
        return str(
            datetime.datetime.now().replace(microsecond=0)
            - obj.updated.replace(tzinfo=None).replace(microsecond=0)
        )

    def get_type(self, obj):
        return "article"

    class Meta:
        model = Article
        fields = [
            "id",
            "type",
            "category",
            "title",
            "content",
            "author",
            "image",
            "updated",
        ]


class NewsFeedCommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField("get_author")
    updated = serializers.SerializerMethodField("get_updated")
    article = serializers.SerializerMethodField("get_article")
    type = serializers.SerializerMethodField("get_type")

    def get_author(self, obj):
        user = obj.user
        serializer = UserShortInfoSerializer(user)
        return serializer.data

    def get_updated(self, obj):
        return str(
            datetime.datetime.now().replace(microsecond=0)
            - obj.updated.replace(tzinfo=None).replace(microsecond=0)
        )

    def get_article(self, obj):
        article = obj.article
        serializer = NewsFeedArticleShortSerializer(article)
        return serializer.data

    def get_type(self, obj):
        return "comment"

    class Meta:
        model = Comment
        fields = ["id", "type", "author", "content", "article", "updated"]


class NewsFeedLikeSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField("get_content_type")
    user = serializers.SerializerMethodField("get_user")

    def get_content_type(self, obj):
        article_content_type = 17
        comment_content_type = 19
        if obj.content_type.id == article_content_type:
            article = Article.objects.get(id=obj.object_id)
            serializer = NewsFeedArticleSerializer(article)
            return serializer.data

        if obj.content_type.id == comment_content_type:
            comment = Comment.objects.get(id=obj.object_id)
            serializer = NewsFeedCommentSerializer(comment)
            return serializer.data

    def get_user(self, obj):
        user = obj.user
        serializer = UserShortInfoSerializer(user)
        return serializer.data

    class Meta:
        model = Like
        fields = ["id", "user", "content_type", "object_id", "vote", "date"]


class NewsFeedFollowerSerializer(serializers.ModelSerializer):
    subscriber = serializers.SerializerMethodField("get_subscriber")
    date = serializers.SerializerMethodField("get_date")

    def get_subscriber(self, obj):
        subscriber = obj.subscriber
        serializer = UserShortInfoSerializer(subscriber)
        return serializer.data

    def get_date(self, obj):
        return str(
            datetime.datetime.now().replace(microsecond=0)
            - obj.date.replace(tzinfo=None).replace(microsecond=0)
        )

    class Meta:
        model = Follower
        fields = ["id", "subscriber", "date"]


# class NewsFeedSerializer(serializers.ModelSerializer):
#     article_set = serializers.SerializerMethodField("get_articles")
#     comment_set = serializers.SerializerMethodField("get_comments")
#     following = serializers.SerializerMethodField("get_followers")
#     user_likes = serializers.SerializerMethodField("get_likes")
#
#     def get_articles(self, obj):
#         articles = Article.objects.filter(~Q(author__id=obj.id)).order_by("updated")
#         serializer = NewsFeedBlogSerializer(articles, many=True)
#         return serializer.data
#
#     def get_comments(self, obj):
#         comments = Comment.objects.filter(~Q(user__id=obj.id)).order_by("updated")
#         serializer = NewsFeedCommentSerializer(comments, many=True)
#         return serializer.data
#
#     def get_followers(self, obj):
#         followers = Follower.objects.filter(to_user=obj.id).order_by("date")
#         serializer = NewsFeedFollowerSerializer(followers, many=True)
#         return serializer.data
#
#     def get_likes(self, obj):
#         likes = Like.objects.filter(~Q(user=obj.id)).order_by("date")
#         serializer = NewsFeedLikeSerializer(likes, many=True)
#         return serializer.data
#
#     class Meta:
#         model = User
#         fields = ['id', 'article_set', 'comment_set', 'following', 'user_likes']
