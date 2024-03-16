from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django_summernote.admin import SummernoteModelAdmin

from actions.models import Like

from .models import Article, Category, Comment


class LikeContentTypeInline(GenericStackedInline):
    model = Like
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment


@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    search_fields = ('title',)
    list_display = ('title', 'category', 'status', 'author')
    summernote_fields = ('content',)
    fields = ('category', 'title', 'status', 'author', 'image', 'content', 'created', 'updated')
    readonly_fields = ('created', 'updated')
    list_select_related = ('category', 'author')
    list_filter = ('status',)
    inlines = [
        CommentInline,
        LikeContentTypeInline,
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'created')
    list_filter = ('created',)
    search_fields = ('user',)
    summernote_fields = ('content',)
    readonly_fields = ('created', 'updated')
    list_select_related = ('user', 'article')
    inlines = [
        LikeContentTypeInline,
    ]
