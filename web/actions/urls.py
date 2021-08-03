from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'actions'

router = DefaultRouter()

urlpatterns = [
    path('', views.FollowerView.as_view(), name="action"),
]

urlpatterns += router.urls
