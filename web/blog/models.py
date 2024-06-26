from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse_lazy

from actions.choices import LikeChoice
from actions.models import Like

from .choices import ArticleStatus

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ("-id",)

    def save(self, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        return super().save(**kwargs)


class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="article_set")
    title = models.CharField(max_length=200)
    # comment = models.ForeignKey('Comment', on_delete=models.SET_NULL, null=True, related_name='article_set')
    slug = models.SlugField(max_length=200, allow_unicode=True, unique=True)  # makes url more readable
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="article_set")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField(choices=ArticleStatus.choices, default=ArticleStatus.INACTIVE)
    image = models.ImageField(upload_to="articles/", blank=True, default="no-image-available.jpg")
    objects = models.Manager()
    votes = GenericRelation(Like, related_query_name="articles")

    @property
    def short_title(self):
        return self.title[:30]

    def __str__(self):
        return "{title} - {author}".format(title=self.short_title, author=self.author)

    def save(self, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        return super().save(**kwargs)

    def get_absolute_url(self):
        url = "blog:post-detail"
        return reverse_lazy(url, kwargs={"slug": self.slug})

    def likes(self):
        return self.votes.aggregate(count=models.Count("vote", filter=models.Q(vote=LikeChoice.LIKE)))

    def dislikes(self):
        return self.votes.aggregate(count=models.Count("vote", filter=models.Q(vote=LikeChoice.DISLIKE)))

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ("-updated", "-created", "id")


DEFAULT_PARENT_COMMENT_ID = 1


class Comment(models.Model):
    # parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, default=DEFAULT_PARENT_COMMENT_ID)
    author = models.EmailField()
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="comment_set",
        blank=True,
    )
    content = models.TextField(max_length=200)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comment_set")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    votes = GenericRelation(Like, related_query_name="comments")
    objects = models.Manager()

    def likes(self):
        return self.votes.aggregate(count=models.Count("vote", filter=models.Q(vote=LikeChoice.LIKE)))

    def dislikes(self):
        return self.votes.aggregate(count=models.Count("vote", filter=models.Q(vote=LikeChoice.DISLIKE)))

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
