from django.urls import path
from . import views

urlpatterns = [
    # List all trainers
    path('trainers/', views.trainer_list, name='trainer_list'),

    # Select a trainer by ID and save to the user's profile
    path('select_trainer/<int:trainer_id>/', views.select_trainer, name='select_trainer'),

    # Show the selected trainer's details (no arguments needed)
    path('my_trainer/', views.my_trainer, name='my_trainer'),

    # Trainer dashboard
    path('dashboard/', views.trainer_dashboard, name='trainer_dashboard'),  # This should be the path to dashboard
]
