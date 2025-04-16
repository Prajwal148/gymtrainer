from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.profile_create, name='profile_create'),
    path('edit/<int:pk>/', views.profile_update, name='profile_update'),
    path('profile/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('diet-plan/<int:pk>/', views.generate_diet_plan, name='generate_diet_plan'),
    path('workout-plan/<int:pk>/', views.generate_workout_plan, name='generate_workout_plan'),
]
