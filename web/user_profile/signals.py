import os

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from django.contrib.auth import get_user_model
from .models import Profile
from .services import UserProfileService

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, created: bool, instance, **kwargs):
    print(sender, created, instance, kwargs, 'SIGNAL')
    if created:
        Profile.objects.create(user=instance)


@receiver(pre_save, sender=Profile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_image = Profile.objects.get(pk=instance.pk).image
    except Profile.DoesNotExist:
        return False

    new_image = instance.image
    # print(os.path.dirname(old_image.path))
    if not old_image == new_image:
        if os.path.isfile(old_image.path) and os.path.dirname(old_image.path) != '/usr/src/web/media':
            os.remove(old_image.path)
