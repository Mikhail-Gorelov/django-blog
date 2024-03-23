from blog.models import Category
from blog.serializers import CategorySerializer
from django import template

register = template.Library()


@register.simple_tag
def categories_list():
    queryset = Category.objects.all()[:7]
    serializer = CategorySerializer(queryset, many=True)
    return serializer.data
