from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'actions'

router = DefaultRouter()

urlpatterns = [
    path('follow/', views.FollowerView.as_view(), name="follow"),
    path('assessment/', views.AssessmentView.as_view(), name="assessment"),
    path('article-rating/', views.ArticleRating.as_view(), name="popular_articles")
]

urlpatterns += router.urls
