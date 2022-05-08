import logging

from django.core.cache import cache
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from blog.pagination import StandardResultsSetPagination
from blog.serializers import CommentSerializer
from main.pagination import BasePageNumberPagination

from . import pagination, serializers
from .filters import ArticleFilter
from .services import BlogService

logger = logging.getLogger(__name__)


class ViewSet(ModelViewSet):
    http_method_names = ('get', 'post', 'put', 'delete')
    lookup_field = 'slug'
    permission_classes = (AllowAny,)
    pagination_class = BasePageNumberPagination


class CategoryViewSet(ViewSet):
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        categories = cache.get('categories')
        if categories is None:
            categories = BlogService.category_queryset()
            cache.set('categories', categories)
        return categories


class ArticleViewSet(ViewSet):
    filterset_class = ArticleFilter
    permission_classes = (AllowAny,)
    pagination_class = StandardResultsSetPagination

    def get_template_name(self):
        if self.action == 'list':
            return 'blog/post_list.html'
        elif self.action == 'retrieve':
            return 'blog/post_detail.html'

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ArticleSerializer
        return serializers.FullArticleSerializer

    def get_queryset(self):
        posts = cache.get('posts')
        if posts is None:
            posts = BlogService.get_active_articles()
            cache.set('posts', posts)
        return posts

    def list(self, request, **kwargs):
        queryset = self.get_queryset()
        response = super().list(request, **kwargs)
        response.template_name = self.get_template_name()

        print(queryset)
        return response

    def retrieve(self, request, **kwargs):
        response = super().retrieve(request, **kwargs)
        response.template_name = self.get_template_name()
        return response


class CommentViewSet(ListModelMixin, GenericViewSet):
    pagination_class = StandardResultsSetPagination
    permission_classes = (AllowAny,)

    # article_id = serializers.ArticleSerializer.id

    def get_template_name(self):
        return 'blog/includes/comments.html'

    def get_serializer_class(self):
        return CommentSerializer

    def get_queryset(self):
        print(self.kwargs)
        return BlogService.comment_queryset(article_id=self.kwargs.get("article_id"))

    def list(self, request, article_id, *args, **kwargs):
        response = super().list(request, **kwargs)
        response.template_name = self.get_template_name()
        return response
