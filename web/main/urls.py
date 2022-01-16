from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import RedirectView
from django.conf import settings

from . import views

urlpatterns = [
    path('user/', views.UserView.as_view()),
    path('timezone/set/', views.SetUserTimeZone.as_view(), name='set_user_timezone'),
    path('jwt/callback/', views.ValidateJWTView.as_view(), name='validate-jwt'),
    path('chat/user-information/', views.ReturnUserInfoView.as_view(), name='user-information'),
]

if settings.ENABLE_RENDERING:
    urlpatterns += [path('', views.TemplateAPIView.as_view(template_name='index.html'), name='index')]
else:
    urlpatterns += [path('', login_required(RedirectView.as_view(pattern_name='admin:index')))]
