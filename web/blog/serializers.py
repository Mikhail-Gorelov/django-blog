from rest_framework import serializers

from main.serializers import UserSerializer

from .models import Article, Category, Comment


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True, allow_unicode=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class ArticleSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url')
    author = UserSerializer()
    category = CategorySerializer()
    comments_count = serializers.IntegerField()
    id = serializers.IntegerField()

    class Meta:
        model = Article
        fields = ('title', 'url', 'author', 'category', 'created', 'updated', 'comments_count', 'id')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'author', 'content', 'updated', 'article', 'user')


class FullArticleSerializer(ArticleSerializer):
    comments = CommentSerializer(source='comment_set', many=True)

    class Meta(ArticleSerializer.Meta):
        fields = ArticleSerializer.Meta.fields + (
            'content',
            'comments',
        )
