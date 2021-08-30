from django.conf import settings
from rest_framework.reverse import reverse_lazy
from django.db.models import Count

from .choices import ArticleStatus
from .models import Category, Article, Comment


class BlogService:

    @staticmethod
    def category_queryset():
        return Category.objects.all()

    @staticmethod
    def comment_queryset(article_id):
        return Comment.objects.filter(article_id=article_id)

    @staticmethod
    def get_active_articles():
        return Article.objects.select_related('category').filter(status=ArticleStatus.ACTIVE).\
            annotate(comments_count=Count('comment_set'))
