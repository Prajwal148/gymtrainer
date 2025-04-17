from django.db import models
from django.contrib.auth.models import User

from gym_trainer import settings


class Trainer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trainer')
    Firstname = models.CharField(max_length=100)
    Lastname = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='trainers/', blank=True, null=True)

    def __str__(self):
        return f"{self.Firstname} {self.Lastname}"

