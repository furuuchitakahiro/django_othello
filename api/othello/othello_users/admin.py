from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from othello_users.models import OthelloUser


@admin.register(OthelloUser)
class UserAdmin(_UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'slug')}),
        (_('Personal info'), {'fields': ('email',)}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions'
        )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2'
            ),
        }),
    )

    list_display = ('username', 'email', 'is_staff')
    search_fields = ('username', 'email')
    filter_horizontal = ('groups', 'user_permissions')
