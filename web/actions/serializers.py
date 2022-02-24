from rest_framework import serializers
from . import choices
from .services import ActionsService
from .models import Follower, Like
from blog.models import Article


# Create your serializers here.


class FollowerSerializer(serializers.ModelSerializer):
    to_user = serializers.IntegerField(min_value=1)

    class Meta:
        model = Follower
        fields = ('to_user',)

    def save(self):
        if self.validated_data["to_user"] is None:
            self.to_user = 296
        else:
            self.validated_data["to_user"] = None
        # 1) проверка на существование записи
        # 2) если записи нет
        # 3) создаём подписку
        # 4) иначе удаляем подписку
        print(self.validated_data)
        # return to_user_instance

    @property
    def data(self):
        return self.validated_data


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
