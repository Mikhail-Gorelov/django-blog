from allauth.account.models import EmailAddress
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

User = get_user_model()


class EmailsInline(admin.TabularInline):
    """Class for inherit emails table to UserAdmin"""

    model = EmailAddress
    can_delete = False
    extra = 1

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False if obj else True


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ('-id',)
    list_display = ('email', 'full_name', 'is_active', 'email_verified')
    search_fields = ('first_name', 'last_name', 'email')
    inlines = (EmailsInline,)

    fieldsets = (
        (_('Personal info'), {'fields': ('id', 'first_name', 'last_name', 'email')}),
        (_('Secrets'), {'fields': ('password',)}),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
            },
        ),
    )
    readonly_fields = ('id',)
    actions = ('delete_selected_users',)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def delete_selected_users(self, request, queryset):
        users_ids = queryset.values_list("id", flat=True)
        OutstandingToken.objects.filter(user_id__in=users_ids).delete()
        queryset.delete()


title = settings.MICROSERVICE_TITLE

admin.site.site_title = title
admin.site.site_header = title
admin.site.site_url = '/'
admin.site.index_title = title

admin.site.unregister(Group)
