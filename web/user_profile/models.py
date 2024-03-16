from urllib.parse import urljoin

# from django_prometheus.models import ExportModelOperationsMixin
from django.contrib.auth import get_user_model
from django.db import models

from src import settings

from . import choices, managers

User = get_user_model()


# Create your models here.
# class Profile(ExportModelOperationsMixin('profile'), models.Model):
class Profile(models.Model):
    objects = models.Manager()
    gender = models.IntegerField(choices=choices.GenderChoice.choices, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(
        upload_to="profile/", default="default_avatar.jpg"
    )  # height_field=100, width_field=100)
    birthdate = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=2000, help_text="Bio", default="")
    website = models.URLField(max_length=300, default="", blank=True)

    def avatar_url(self):
        return urljoin(settings.BACKEND_SITE, self.image.url)

    def __str__(self):
        return str(self.user.full_name())
