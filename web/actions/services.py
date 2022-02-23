from django.conf import settings
from typing import Union, Optional
from .models import Like
from . import choices
from django.contrib.contenttypes.models import ContentType
from blog.models import Comment, Article
from typing import TYPE_CHECKING
from main.models import UserType

if TYPE_CHECKING:
    from main.models import UserType


class ActionsService:
    @staticmethod
    def get_like_object(like_type: str, object_id: int) -> Union[Article, Comment]:
        if like_type == choices.LikeTypeChoice.ARTICLE:
            return Article.objects.get(id=object_id)
        if like_type == choices.LikeTypeChoice.COMMENT:
            return Comment.objects.get(id=object_id)

    @staticmethod
    def get_content_object(model_object: Union[Article, Comment]) -> ContentType:
        return ContentType.objects.get_for_model(model_object)

    @staticmethod
    def get_like(user: UserType, obj: Union[Article, Comment], object_id: int) -> Optional[Like]:
        content_type = ActionsService.get_content_object(obj)
        try:
            return Like.objects.get(user=user, content_type=content_type, object_id=object_id)
        except Like.DoesNotExist:
            return None

