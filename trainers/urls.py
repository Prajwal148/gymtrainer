from django.urls import path
from . import views
from .views import create_trainer, update_trainer, trainer_detail

urlpatterns = [
    path('trainers/', views.trainer_list, name='trainer_list'),
    path('select_trainer/<int:trainer_id>/', views.select_trainer, name='select_trainer'),
    path('my_trainer/', views.my_trainer, name='my_trainer'),
    path('dashboard/', views.trainer_dashboard, name='trainer_dashboard'),
    path('create/', create_trainer, name='trainer_create'),
    path('<int:pk>/', trainer_detail, name='trainer_detail'),      # ✅ View profile
    path('<int:pk>/edit/', update_trainer, name='trainer_update'), # ✅ Edit profile
]
