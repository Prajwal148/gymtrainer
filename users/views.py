from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserCreateForm
from django.contrib.auth.decorators import login_required

def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_trainer:
                return redirect('trainer_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})
def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('users:login')
    else:
        form = UserCreateForm()
    return render(request, 'users/signup.html', {'form': form})