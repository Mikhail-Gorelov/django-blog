from django.db import models
from django.contrib.auth import get_user_model
from . import managers

User = get_user_model()


# Create your models here.
class Follower(models.Model):
    objects = models.Manager()
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    date = models.DateTimeField(auto_now_add=True)
