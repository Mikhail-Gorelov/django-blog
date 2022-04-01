from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .yasg import urlpatterns as swagger_url

admin_url = settings.ADMIN_URL

urlpatterns = [
    path('actions/', include('actions.urls')),
    path('user-profile/', include('user_profile.urls')),
    path('', include('main.urls')),
    path('auth/', include('auth_app.urls')),
    path('', include('blog.urls')),
    path('', include('contact_us.urls')),
    # path('', include('django_prometheus.urls')),
    path(f'{admin_url}/', admin.site.urls),
    path(f'{admin_url}/defender/', include('defender.urls')),
    path('api/', include('rest_framework.urls')),
    path('rosetta/', include('rosetta.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('about/', include('about.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += swagger_url

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    if settings.ENABLE_SILK:
        urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
    if settings.ENABLE_DEBUG_TOOLBAR:
        from debug_toolbar import urls

        urlpatterns += [path('__debug__/', include(urls))]
