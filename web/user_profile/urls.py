from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'user_profile'

router = DefaultRouter()

router.register('profile', views.ProfileViewSet)
router.register('user', views.UserViewSet)


urlpatterns = [
    path('', views.ProfileViewSet.as_view({'get': 'profile'}), name='user-profile')
]

urlpatterns += [
    path('true-users/', views.TrueUserViewSet.as_view({'get': 'user_list'}), name='api_list_true_users'),
    path('password-change/', views.UserViewSet.as_view({"post": 'password_change'}), name='password_change'),
    path('update-image/', views.UserViewSet.as_view({"post": 'update_image'}), name='update_image'),
    path('<user_id>/', views.ProfileViewSet.as_view({"get": "list"}), name='user_profile'),
]

urlpatterns += router.urls
