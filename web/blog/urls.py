from django.conf import settings
from django.urls import path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from . import views

app_name = "blog"

router = DefaultRouter()
router.register("categories", views.CategoryViewSet, basename="categories")
router.register("posts", views.ArticleViewSet, basename="post")

urlpatterns = [
    path(
        "comments/<article_id>/",
        views.CommentViewSet.as_view({"get": "list"}),
        name="article_comments",
    ),
]

urlpatterns += router.urls
