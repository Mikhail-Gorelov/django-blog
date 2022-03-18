import logging
import os

from dj_rest_auth import views as auth_views
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, BasePermission, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from . import serializers, services
from .models import Profile
from .services import UserProfileService

User = get_user_model()
logger = logging.getLogger(__name__)


class ViewSet(ModelViewSet):
    # http_method_names = ('get', 'put')
    # permission_classes = (AllowAny,)

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = (IsAuthenticatedOrReadOnly,)
        else:
            permission_classes = (AllowAny,)
        return [permission() for permission in permission_classes]


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


class ProfileViewSet(ViewSet, RetrieveModelMixin, UserViewSet):
    template_name = "user-profile.html"
    serializer_class = serializers.UserProfileSerializer
    lookup_field = "id"

    def profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(
            {
                "user": serializer.data,
                "CHAT_SITE_INIT": os.environ.get("CHAT_SITE_INIT")
            },
            template_name=self.template_name,
        )

    def perform_create(self, serializer):
        serializer.save()

    # def get_queryset(self):
    #     print(self.kwargs)
    #     return UserProfileService.get_user_profile_queryset(user_id=self.kwargs.get("id"))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
        # response = super().list(request, **kwargs)
        # response.template_name = self.template_name
        # return response


class TrueUserViewSet(viewsets.GenericViewSet):
    template_name = "user-list.html"  # страница со списком пользователей
    serializer_class = serializers.TrueUserSerializer

    def get_queryset(self):
        true_users = cache.get('true_users')
        if true_users is None:
            true_users = UserProfileService.get_user_queryset()
            cache.set('true_users', true_users, timeout=120)
        return true_users

    def user_list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(
            {"users": serializer.data, "CHAT_SITE_INIT": os.environ.get("CHAT_SITE_INIT")},
            template_name=self.template_name,
        )

    def perform_create(self, serializer):
        serializer.save()


class ProfileSettingsView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.ProfileUpdateSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.kwargs['user_id'])
        return obj

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(id=self.kwargs['user_id'])


class ProfileSettingsRetrieveViewSet(viewsets.GenericViewSet):
    template_name = 'profile-settings.html'
    serializer_class = serializers.ProfileUpdateSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = 'user_id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
