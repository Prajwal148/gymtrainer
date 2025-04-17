from django.db import models
from django.contrib.auth.models import User
from datetime import date

from gym_trainer import settings
from trainers.models import Trainer  # Import the Trainer model


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # in cm
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # in kg
    smoking = models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)
    alcohol = models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)

    FOOD_CHOICES = [
        ('vegetarian', 'Vegetarian'),
        ('non-vegetarian', 'Non-Vegetarian'),
        ('vegan', 'Vegan')
    ]
    food_habits = models.CharField(max_length=20, choices=FOOD_CHOICES, default='non-vegetarian')

    WORKOUT_EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ]
    workout_experience = models.CharField(max_length=20, choices=WORKOUT_EXPERIENCE_CHOICES, default='beginner')

    # Store user-specific diet and workout plans as JSON
    diet_plan = models.JSONField(blank=True, null=True)
    workout_plan = models.JSONField(blank=True, null=True)

    # Trainer relationship
    selected_trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def calculate_age(self):
        if not self.date_of_birth:
            return "Not set"
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def calculate_bmi(self):
        if self.height and self.weight:
            height_m = float(self.height) / 100  # Convert to meters
            return round(float(self.weight) / (height_m ** 2), 2)
        return 0.0

    def get_bmi_label(self):
        bmi = self.calculate_bmi()
        if bmi == 0.0:
            return "Not available"
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 24.9:
            return "Normal"
        elif bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"

    def __str__(self):
        return f"{self.user.username} Profile"
