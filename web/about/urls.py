from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'about'

router = DefaultRouter()

urlpatterns = [
    url('', views.TemplateAPIView.as_view(template_name='about/about_list.html'), name='my_about'),
]

urlpatterns += router.urls
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
