from django.db import models
from django.utils.translation import gettext_lazy as _

from . import managers


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    file = models.FileField(upload_to="feedback/media", null=True, blank=True)

    class Meta:
        verbose_name = _("Feedback")
