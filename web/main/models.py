from typing import TypeVar
from urllib.parse import urljoin

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from actions.choices import LikeChoice

from .managers import UserManager

UserType = TypeVar("UserType", bound="User")


class User(AbstractUser):
    username = None
    email = models.EmailField(_("Email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email

    def full_name(self):
        return super().get_full_name()

    def avatar_url(self):
        return urljoin(settings.BACKEND_SITE, self.profile.image.url)

    def profile_url(self):
        return self.profile.website

    def get_absolute_url(self):
        url = "user_profile:user_profile_id"
        return urljoin(settings.BACKEND_SITE, str(reverse_lazy(url, kwargs={"id": self.id})))

    def email_verified(self):
        return self.emailaddress_set.get(primary=True).verified

    def likes_count(self) -> dict:
        return self.user_likes.aggregate(count=models.Count("like", filter=models.Q(vote=LikeChoice.LIKE)))

    def get_dislikes_count(self) -> dict:
        return self.user_likes.aggregate(
            count=models.Count("dislike", filter=models.Q(vote=LikeChoice.DISLIKE))
        )

    def subscribers_count(self) -> dict:
        return self.followers.aggregate(count=models.Count("to_user"))

    email_verified.boolean = True


class APILogsModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    api = models.CharField(max_length=1024, help_text='API URL')
    headers = models.TextField()
    body = models.TextField()
    method = models.CharField(max_length=10, db_index=True)
    client_ip_address = models.CharField(max_length=50)
    response = models.TextField()
    status_code = models.PositiveSmallIntegerField(help_text='Response status code', db_index=True)
    execution_time = models.DecimalField(
        decimal_places=5, max_digits=8, help_text='Server execution time (Not complete response time.)'
    )
    added_on = models.DateTimeField()

    def __str__(self):
        return self.api

    class Meta:
        verbose_name = 'API Log'
        verbose_name_plural = 'API Logs'
