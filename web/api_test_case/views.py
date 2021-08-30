import logging
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from . import services
from . import serializers
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer

logger = logging.getLogger(__name__)

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
