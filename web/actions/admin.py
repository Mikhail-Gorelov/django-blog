from django.contrib import admin

from .models import Follower


# Register your models here.
@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_filter = ('date',)
    search_fields = ('to_user',)
    list_per_page = 10
    list_display = ('subscriber',)
    list_select_related = ('to_user', 'subscriber')
    list_display_links = ('subscriber',)
