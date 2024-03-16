from rest_framework import serializers
from . import choices
from django.contrib.auth import get_user_model
from .services import ActionsService
from .models import Follower, Like
from blog.models import Article

User = get_user_model()


# Create your serializers here.


class FollowerSerializer(serializers.ModelSerializer):
    to_user = serializers.IntegerField(min_value=1)

    class Meta:
        model = Follower
        fields = ('to_user',)

    def save(self):
        try:
            follower = Follower.objects.get(
                subscriber=self.context["request"].user,
                to_user=User.objects.get(pk=self.validated_data["to_user"]),
            )
            follower.delete()
        except Follower.DoesNotExist:
            Follower.objects.create(
                subscriber=self.context["request"].user,
                to_user=User.objects.get(pk=self.validated_data["to_user"]),
            )
        return

    @property
    def data(self):
        return User.objects.get(pk=self.validated_data["to_user"]).subscribers_count()


class AssessmentSerializer(serializers.Serializer):
    like_type = serializers.ChoiceField(choices=choices.LikeTypeChoice.choices)
    object_id = serializers.IntegerField()
    vote = serializers.ChoiceField(choices=choices.LikeChoice.choices)

    def save(self, **kwargs):
        user = self.context['request'].user
        vote: int = self.validated_data["vote"]
        like_type: str = self.validated_data["like_type"]
        object_id: int = self.validated_data["object_id"]
        obj = ActionsService.get_like_object(like_type, object_id)
        if like := ActionsService.get_like(user, obj, object_id):
            if like.vote == vote:
                like.delete()
            else:
                like.vote = vote
                like.save(update_fields=["vote"])
        else:
            # Like.objects.create(user=user, content_type=, object_id=, vote=)
            obj.votes.create(user=user, vote=vote)

        return_data = {
            "likes_count": obj.likes()["count"],
            "dislike_count": obj.dislikes()["count"],
        }
        return return_data


class ArticleRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'category', 'title', 'content', 'author', 'created', 'updated', 'status', 'image')
