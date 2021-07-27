import logging
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Profile
from .serializers import ProfileSerializer, UserProfileSerializer, TrueUserSerializer, ChangePasswordSerializer
from . import services
from . import serializers
from django.contrib.auth import get_user_model
from user_profile.services import UserProfileService
from dj_rest_auth import views as auth_views

User = get_user_model()
logger = logging.getLogger(__name__)


class UserViewSet(viewsets.GenericViewSet):
    # template_name = "user-profile.html"
    queryset = User.objects.all()

    def get_template_name(self):
        if self.action == 'user':
            return 'user-profile.html'
        elif self.action == 'password_change':
            return 'user_profile/reset_password_email_link.html'
        else:
            return 'user-profile.html'

    def get_serializer_class(self):
        if self.action == 'user':
            return UserProfileSerializer
        if self.action == 'password_change':
            return ChangePasswordSerializer
        return UserProfileSerializer

    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": "changed successfully"})

    def user(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, template_name=self.template_name)


class ProfileViewSet(UserViewSet, viewsets.GenericViewSet):
    template_name = "user-profile.html"
    serializer_class = UserProfileSerializer

    def profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, template_name=self.template_name)

    def perform_create(self, serializer):
        serializer.save()


class TrueUserViewSet(viewsets.GenericViewSet):
    template_name = "user-list.html"  # страница со списком пользователей
    serializer_class = TrueUserSerializer

    def get_queryset(self):
        return UserProfileService.get_user_queryset()

    def user_list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({"users": serializer.data}, template_name=self.template_name)

    def perform_create(self, serializer):
        serializer.save()
