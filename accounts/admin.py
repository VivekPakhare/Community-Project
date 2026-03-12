from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'college', 'role', 'is_verified', 'is_active']
    list_filter = ['role', 'is_verified', 'is_active', 'college']
    search_fields = ['username', 'email', 'college']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile', {'fields': ('phone', 'college', 'role', 'is_verified', 'avatar', 'bio')}),
    )
