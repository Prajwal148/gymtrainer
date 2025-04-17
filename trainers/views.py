from django.shortcuts import render, redirect, get_object_or_404

from .forms import TrainerForm
from .models import Trainer
from django.contrib.auth.decorators import login_required
from userprofile.models import UserProfile


# List all trainers
def trainer_list(request):
    trainers = Trainer.objects.all()
    return render(request, 'trainers/trainer_list.html', {'trainers': trainers})

# Select a trainer and save the selected trainer to the user's profile
@login_required
def select_trainer(request, trainer_id):
    trainer = Trainer.objects.get(id=trainer_id)

    request.user.userprofile.selected_trainer = trainer
    request.user.userprofile.save()

    return redirect('my_trainer')

# Display the user's selected trainer
@login_required
def my_trainer(request):
    user_profile = request.user.userprofile
    trainer = user_profile.selected_trainer

    if trainer:
        return render(request, 'trainers/trainer_detail.html', {'trainer': trainer})
    else:
        return redirect('trainer_list')


@login_required
def trainer_dashboard(request):
    # Only trainers can access this page
    print(request.user.userprofile.is_trainer)
    if not request.user.userprofile.is_trainer:
        return redirect('home')  # If the user is not a trainer, redirect to the homepage


    # Get all users who have selected the logged-in user as their trainer
    users = UserProfile.objects.filter(selected_trainer=request.user.userprofile)

    # Handle user selection from dropdown
    selected_user = None
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        selected_user = get_object_or_404(UserProfile, id=user_id)

    return render(request, 'trainers/trainer_dashboard.html', {
        'users': users,
        'selected_user': selected_user
    })

@login_required
def create_trainer(request):
    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES)
        if form.is_valid():
            trainer = form.save(commit=False)
            trainer.user = request.user
            trainer.save()
            return redirect('trainer_detail', trainer_id=trainer.id)
    else:
        form = TrainerForm()
    return render(request, 'trainers/trainer_create.html', {'form': form})