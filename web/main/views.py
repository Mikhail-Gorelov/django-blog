from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.parsers import FormParser
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from user_profile import serializers as user_profile_serializer
from rest_framework.authentication import SessionAuthentication
from user_profile import models as user_profile_models
from . import models
from allauth.account.models import EmailAddress
from src.celery import app

from .serializers import UserSerializer, SetTimeZoneSerializer, ValidateJWTSerializer, ReturnUsersSerializer

User = get_user_model()


class TemplateAPIView(APIView):
    """ Help to build CMS System using DRF, JWT and Cookies
        path('some-path/', TemplateAPIView.as_view(template_name='template.html'))
    """
    permission_classes = (AllowAny,)
    template_name = ''

    @method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
    def get(self, request, *args, **kwargs):
        return Response()


class UserView(GenericAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), id=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request):
        """Current user view

            Using this construction you can load related fields (select_related and prefetch_related) in queryset
        """

        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)


class SetUserTimeZone(GenericAPIView):
    authentication_classes = (SessionAuthentication,)
    serializer_class = SetTimeZoneSerializer
    parser_classes = (FormParser,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = app.send_task(
            name='main.tasks.add',
            kwargs={'x': 2, 'y': 2},
        )
        print(result)
        response = Response()
        response.set_cookie(
            key=getattr(settings, 'TIMEZONE_COOKIE_NAME', 'timezone'),
            value=serializer.data.get('timezone'),
            max_age=getattr(settings, 'TIMEZONE_COOKIE_AGE', 86400),
        )
        return response


class ValidateJWTView(GenericAPIView):
    serializer_class = ValidateJWTSerializer
    permission_classes = ()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # return Response({"detail": "hello from blog"})
        return Response(serializer.response_data)


class ReturnUserInfoView(GenericAPIView):
    serializer_class = user_profile_serializer.GetUsersIdSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_list = User.objects.filter(pk__in=serializer.data['user_id'])
        users_info = user_profile_serializer.UserShortInfoSerializer(user_list, many=True)
        return Response(users_info.data)
