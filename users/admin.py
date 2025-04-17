from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NewUser

class CustomUserAdmin(UserAdmin):
    model = NewUser

    list_display = ('username', 'email', 'is_staff', 'is_active', 'is_trainer')
    list_filter = ('is_staff', 'is_active', 'is_trainer')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Trainer Info', {'fields': ('is_trainer',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_trainer', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(NewUser, CustomUserAdmin)
