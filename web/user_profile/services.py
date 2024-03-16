from typing import List

from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.auth import get_user_model

from actions.models import Follower
from main.services import MainService

User = get_user_model()


class UserProfileService:
    @staticmethod
    def get_user_queryset():
        return User.objects.filter(
            is_active=True,
            is_staff=False,
            is_superuser=False,
        )
        # return User.objects.all()

    @staticmethod
    def get_user_profile_queryset(user_id):
        return User.objects.filter(
            id=user_id,
        )

    @staticmethod
    def deactivate_email(email: EmailAddress):
        email.verified = False
        if email.primary:
            email.primary = False
        email.save(update_fields=["verified", "primary"])
        return email

    @staticmethod
    def get_subscriptions_to(user: User) -> List[User]:
        following = list(Follower.objects.filter(subscriber=user).values_list("to_user", flat=True))
        return User.objects.filter(id__in=following)
