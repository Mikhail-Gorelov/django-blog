import logging
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Profile
from . import services
from . import serializers
from django.contrib.auth import get_user_model
from .services import UserProfileService
from dj_rest_auth import views as auth_views
from rest_framework.parsers import MultiPartParser

User = get_user_model()
logger = logging.getLogger(__name__)


class UserViewSet(viewsets.GenericViewSet):
    # template_name = "user-profile.html"
    queryset = User.objects.all()
    # parser_classes = [MultiPartParser]

    def get_template_name(self):
        if self.action == 'user':
            return 'user-profile.html'
        elif self.action == 'password_change':
            return 'user_profile/reset_password_email_link.html'
        else:
            return 'user-profile.html'

    def get_serializer_class(self):
        if self.action == 'user':
            return serializers.UserProfileSerializer
        if self.action == 'password_change':
            return serializers.ChangePasswordSerializer
        if self.action == "update_image":
            return serializers.ChangeImageSerializer
        return serializers.UserProfileSerializer

    def update_image(self, request):
        serializer = self.get_serializer(data=request.data, instance=request.user.profile)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": "changed successfully"})

    def user(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, template_name=self.template_name)


class ProfileViewSet(ListModelMixin, UserViewSet, viewsets.GenericViewSet):
    template_name = "user-profile.html"
    serializer_class = serializers.UserProfileSerializer

    def profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, template_name=self.template_name)

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        print(self.kwargs)
        return UserProfileService.get_user_profile_queryset(id=self.kwargs.get("id"))

    def list(self, request, user_id, *args, **kwargs):
        response = super().list(request, **kwargs)
        response.template_name = self.template_name
        return response


class TrueUserViewSet(viewsets.GenericViewSet):
    template_name = "user-list.html"  # страница со списком пользователей
    serializer_class = serializers.TrueUserSerializer

    def get_queryset(self):
        return UserProfileService.get_user_queryset()

    def user_list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({"users": serializer.data}, template_name=self.template_name)

    def perform_create(self, serializer):
        serializer.save()
