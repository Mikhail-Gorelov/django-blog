from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'actions'

router = DefaultRouter()

urlpatterns = [
    path('follow/', views.FollowerView.as_view(), name="follow"),
]

urlpatterns += router.urls
