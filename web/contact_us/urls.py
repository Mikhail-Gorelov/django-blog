from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter

from main.views import TemplateAPIView

from . import views

app_name = "contact_us"

router = DefaultRouter()

urlpatterns = [path("feedback/", views.FeedbackView.as_view(), name="api_feedback")]

urlpatterns += router.urls

if settings.ENABLE_RENDERING:
    urlpatterns += [
        path(
            "contact/",
            TemplateAPIView.as_view(template_name="contact_us/index.html"),
            name="index",
        ),
    ]
