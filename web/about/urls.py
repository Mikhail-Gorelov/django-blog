from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

app_name = 'about'

router = DefaultRouter()

urlpatterns = [
    url('', views.AboutListView.as_view(), name='my_about'),
]

urlpatterns += router.urls
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
