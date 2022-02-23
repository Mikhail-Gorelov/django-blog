import logging

from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from . import serializers, services

logger = logging.getLogger(__name__)


# Create your views here.
class FollowerView(GenericAPIView):
    serializer_class = serializers.FollowerSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AssessmentView(GenericAPIView):
    serializer_class = serializers.AssessmentSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)


class ArticleRating(GenericAPIView):
    pass
