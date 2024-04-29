from django.conf import settings
from django.urls import path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from django.views.decorators.cache import cache_page
from main.views import TemplateAPIView

from . import views

app_name = "auth_app"

router = DefaultRouter()

urlpatterns = [
    path("token/refresh/", TokenRefreshView.as_view()),
    path("token/verify/", TokenVerifyView.as_view()),
]

urlpatterns += [
    path("sign-in/", views.LoginView.as_view(), name="api_login"),
    path("sign-up/", views.SignUpView.as_view(), name="api_sign_up"),
    path("sign-up/verify/", views.VerifyEmailView.as_view(), name="api_sign_up_verify"),
    path("password/reset/", views.PasswordResetView.as_view(), name="api_forgot_password"),
    path(
        "password/reset/confirm/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm_email",
    ),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]

urlpatterns += router.urls

urlpatterns += [
    path(
        "password-reset/<uidb64>/<token>/",
        TemplateView.as_view(template_name="auth_app/includes/reset_password_email_link.html"),
        name="password_reset_confirm",
    ),
    path(
        "verify-email/<key>/",
        TemplateAPIView.as_view(template_name="auth_app/success_enter_link.html"),
        name="account_verification",
    ),
]

if settings.ENABLE_RENDERING:
    urlpatterns += [
        path(
            "login/",
            cache_page(60 * 10)(TemplateAPIView.as_view(template_name="auth_app/login.html")),
            name="login",
        ),
        path(
            "register/",
            cache_page(60 * 10)(TemplateAPIView.as_view(template_name="auth_app/sign_up.html")),
            name="sign_up",
        ),
        path(
            "verify-email/success",
            TemplateAPIView.as_view(template_name="auth_app/includes/success_enter_link_modal.html"),
            name="verify_email_success",
        ),
        path(
            "password-recovery/",
            TemplateAPIView.as_view(template_name=""),
            name="password_recovery",
        ),
        path(
            "password-sent/",
            TemplateAPIView.as_view(template_name="auth_app/reset_password_sent.html"),
            name="reset_email_sent",
        ),
    ]
