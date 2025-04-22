from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Department
from departments.models import Team

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'department', 'is_staff')
    list_filter = ('role', 'department', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 'date_of_birth', 'profile_picture')}),
        ('Employment Info', {'fields': ('role', 'department', 'joining_date')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'department'),
        }),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Department)
admin.site.register(Team)