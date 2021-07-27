from django.conf import settings
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
        return Article.objects.filter(status=ArticleStatus.ACTIVE).annotate(comments_count=Count('comment_set'))
