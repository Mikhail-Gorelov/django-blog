from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Feedback
from .services import ContactUsService


@receiver(post_save, sender=Feedback)
def send_feedback_email(sender, created: bool, instance, **kwargs):
    print(sender, created, instance, kwargs, 'SIGNAL')
    if created:
        ContactUsService.send_contact_us_email(instance)
