from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from . import models


def clear_category_cache():
    cache.delete("categories")


@receiver(post_delete, sender=models.Category)
def category_post_delete_handler(sender, **kwargs):
    clear_category_cache()


@receiver(post_save, sender=models.Category)
def category_post_save_handler(sender, **kwargs):
    if kwargs["created"]:
        clear_category_cache()


def clear_post_cache():
    cache.delete("posts")


@receiver(post_delete, sender=models.Article)
def posts_post_delete_handler(sender, **kwargs):
    clear_post_cache()


@receiver(post_save, sender=models.Article)
def posts_post_save_handler(sender, **kwargs):
    if kwargs["created"]:
        clear_post_cache()
