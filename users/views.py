from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import UserCreateForm

def signup(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Capture the user type and set is_trainer accordingly
            user_type = request.POST.get('user_type')  # Get the value of selected radio button
            if user_type == 'trainer':
                user.is_trainer = True
            else:
                user.is_trainer = False

            user.save()  # Save the user to the database

            # Redirect to login page or dashboard as per your flow
            return redirect('users:login')  # Replace with your desired URL name
    else:
        form = UserCreateForm()

    return render(request, 'users/signup.html', {'form': form})
