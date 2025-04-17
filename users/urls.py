from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.custom_login_view, name='login'),  # ← custom login view with redirect logic
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
