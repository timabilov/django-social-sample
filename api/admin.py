from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from api.models import UserProfile


class CustomUserAdmin(UserAdmin):
    model = UserProfile
    list_display = UserAdmin.list_display + ('last_seen',)
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': (
                'banned', 'facebook_id', 'google_id', 'ip', 'bio'
            )}),
    )


admin.site.register(UserProfile, CustomUserAdmin)
