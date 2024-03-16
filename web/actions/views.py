import logging

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from blog.models import Article

from . import serializers

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
    serializer_class = serializers.ArticleRatingSerializer
    queryset = Article.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(
            reversed(sorted(queryset, key=lambda a: a.likes()["count"] - a.dislikes()["count"])),
            many=True,
        )
        return Response(serializer.data)
