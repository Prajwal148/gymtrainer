# trainers/admin.py
from django.contrib import admin
from .models import Trainer, UserProfile

# Registering Trainer with a custom admin class
admin.site.register(Trainer)

# Registering UserProfile without a custom admin class
admin.site.register(UserProfile)
