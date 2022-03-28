import json
import logging

import django
import requests
from dj_rest_auth import views as auth_views
from dj_rest_auth.registration.views import VerifyEmailView as _VerifyEmailView
from django.contrib.auth import logout as django_logout
from django.views.generic.base import TemplateResponseMixin, TemplateView
from rest_framework.generics import CreateAPIView
from rest_framework.serializers import ValidationError
from rest_framework.permissions import AllowAny

from . import serializers
from .services import full_logout

logger = logging.getLogger(__name__)


class LoginView(auth_views.LoginView):
    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        captcha_token = self.request.POST.get("g-recaptcha-response")
        captcha_url = "https://www.google.com/recaptcha/api/siteverify"
        captcha_secret = "6LeQmx8fAAAAAMo_RQroMylU3kkjrSU9r5tLfz9T"
        captcha_data = {
            "secret": captcha_secret,
            "response": captcha_token,
        }
        captcha_server_response = requests.post(url=captcha_url, data=captcha_data)
        captcha_json = json.loads(captcha_server_response.text)
        if not captcha_json['success']:
            raise ValidationError("Invalid captcha, try again")
        return super(LoginView, self).post(request, *args, **kwargs)


class SignUpView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserSignUpSerializer


class PasswordResetView(auth_views.PasswordResetView):
    serializer_class = serializers.PasswordResetSerializer


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    serializer_class = serializers.PasswordResetConfirmSerializer


class VerifyEmailView(_VerifyEmailView):
    def get_serializer(self, *args, **kwargs):
        return serializers.VerifyEmailSerializer(*args, **kwargs)


class LogoutView(auth_views.LogoutView):
    allowed_methods = ('POST', 'OPTIONS')

    def session_logout(self):
        django_logout(self.request)

    def logout(self, request):
        self.session_logout()
        response = full_logout(request)
        return response
