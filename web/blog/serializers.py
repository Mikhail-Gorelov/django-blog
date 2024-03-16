from django.db import models
from rest_framework import serializers

from actions.choices import LikeChoice
from actions.models import Like
from main.serializers import UserSerializer

from .models import Article, Category, Comment


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True, allow_unicode=True)

    class Meta:
        model = Category
        fields = ("id", "name", "slug")


class ArticleSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source="get_absolute_url")
    author = UserSerializer()
    category = CategorySerializer()
    comments_count = serializers.IntegerField()
    id = serializers.IntegerField()
    likes = serializers.SerializerMethodField("get_likes")
    dislikes = serializers.SerializerMethodField("get_dislikes")
    vote = serializers.SerializerMethodField("get_vote")

    def get_likes(self, obj):
        count = obj.votes.aggregate(
            count=models.Count("vote", filter=models.Q(vote=LikeChoice.LIKE))
        )
        return count["count"]

    def get_dislikes(self, obj):
        count = obj.votes.aggregate(
            count=models.Count("vote", filter=models.Q(vote=LikeChoice.DISLIKE))
        )
        return count["count"]

    def get_vote(self, obj):
        try:
            like = Like.objects.get(
                articles=obj, user=self.context["request"].user, content_type=17
            )
            return like.vote
        except Like.DoesNotExist:
            return None

    class Meta:
        model = Article
        fields = (
            "vote",
            "dislikes",
            "likes",
            "title",
            "url",
            "author",
            "category",
            "created",
            "updated",
            "comments_count",
            "id",
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "user", "author", "content", "updated", "article", "user")


class FullArticleSerializer(ArticleSerializer):
    comments = CommentSerializer(source="comment_set", many=True)

    class Meta(ArticleSerializer.Meta):
        fields = ArticleSerializer.Meta.fields + (
            "content",
            "comments",
        )
