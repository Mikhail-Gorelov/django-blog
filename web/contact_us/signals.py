from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Feedback
from .services import ContactUsService


@receiver(post_save, sender=Feedback)
def send_feedback_email(sender, created: bool, instance, **kwargs):
    if created:
        ContactUsService.send_contact_us_email(instance)
