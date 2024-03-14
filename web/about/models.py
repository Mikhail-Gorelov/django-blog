from django.db import models

from . import managers


# Create your models here.
class About(models.Model):
    name = models.CharField(max_length=50, help_text='Description', default='')
    description = models.TextField(max_length=2000, help_text="Description", default='')

    def __str__(self):
        return self.name
