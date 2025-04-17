from django.contrib.auth.models import AbstractUser
from django.db import models  # Correct import for models

class NewUser(AbstractUser):
    is_trainer = models.BooleanField(default=False)
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username


