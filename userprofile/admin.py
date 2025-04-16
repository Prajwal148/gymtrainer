from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'height', 'weight')  # removed created_at
    search_fields = ('first_name', 'last_name', 'pgUser__username')
