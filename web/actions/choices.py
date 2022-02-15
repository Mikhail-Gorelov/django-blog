from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class LikeChoice(IntegerChoices):
    LIKE = (1, _('Like'))
    DISLIKE = (0, _('Dislike'))
