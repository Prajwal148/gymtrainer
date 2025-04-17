# trainers/admin.py
from django.contrib import admin
from .models import Trainer

# Registering Trainer with a custom admin class
admin.site.register(Trainer)

