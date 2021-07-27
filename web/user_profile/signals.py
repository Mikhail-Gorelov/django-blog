from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .models import Profile
from .services import UserProfileService

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, created: bool, instance, **kwargs):
    print(sender, created, instance, kwargs, 'SIGNAL')
    if created:
        Profile.objects.create(user=instance)
