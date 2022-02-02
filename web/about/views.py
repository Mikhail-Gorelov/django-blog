from django.utils.decorators import method_decorator
from django.views import generic
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import About


class TemplateAPIView(APIView):
    """Help to build CMS System using DRF, JWT and Cookies
    path('some-path/', TemplateAPIView.as_view(template_name='template.html'))
    """

    permission_classes = (AllowAny,)
    template_name = ''

    @method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
    def get(self, request, *args, **kwargs):
        return Response()
