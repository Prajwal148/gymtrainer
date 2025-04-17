from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import UserCreateForm


def signup(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_type = request.POST.get('is_trainer')
            user.is_trainer = (user_type == 'True')

            user.save()
            return redirect('users:login')
    else:
        form = UserCreateForm()

    return render(request, 'users/signup.html', {'form': form})
