import os

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, created: bool, instance, **kwargs):
    print(sender, created, instance, kwargs, "SIGNAL")
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
    if not old_image == new_image:
        if os.path.isfile(old_image.path) and os.path.dirname(old_image.path) != "/usr/src/web/media":
            os.remove(old_image.path)


def true_users_post_cache():
    cache.delete("true_users")


@receiver(post_delete, sender=User)
def posts_post_delete_handler(sender, **kwargs):
    true_users_post_cache()


@receiver(post_save, sender=User)
def posts_post_save_handler(sender, **kwargs):
    if kwargs["created"]:
        true_users_post_cache()
