from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TrainerForm
from .models import Trainer
from userprofile.models import UserProfile
import json


# List all trainers
def trainer_list(request):
    trainers = Trainer.objects.all()
    return render(request, 'trainers/trainer_list.html', {'trainers': trainers})


# Select a trainer and save it to the user's profile
@login_required
def select_trainer(request, trainer_id):
    trainer = get_object_or_404(Trainer, id=trainer_id)
    request.user.userprofile.selected_trainer = trainer
    request.user.userprofile.save()
    return redirect('my_trainer')


# Display the user's selected trainer
@login_required
def my_trainer(request):
    trainer = request.user.userprofile.selected_trainer
    if trainer:
        return render(request, 'trainers/trainer_detail.html', {'trainer': trainer})
    return redirect('trainer_list')


# Trainer profile creation
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


@login_required
def trainer_dashboard(request):
    try:
        trainer = request.user.trainer
    except Trainer.DoesNotExist:
        trainer = None

    users = UserProfile.objects.filter(selected_trainer=trainer)
    selected_user = None
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Fetch selected user from either POST or GET
    user_id = request.POST.get('user_id') or request.GET.get('user_id')
    if user_id:
        selected_user = get_object_or_404(UserProfile, id=user_id)

        # Convert JSON strings to dicts if needed
        if isinstance(selected_user.diet_plan, str):
            try:
                selected_user.diet_plan = json.loads(selected_user.diet_plan)
            except json.JSONDecodeError:
                selected_user.diet_plan = {}

        if isinstance(selected_user.workout_plan, str):
            try:
                selected_user.workout_plan = json.loads(selected_user.workout_plan)
            except json.JSONDecodeError:
                selected_user.workout_plan = {}

    # Handle POST submission to update plans
    if request.method == 'POST' and selected_user:
        if any(key.startswith('diet_') or key.startswith('workout_') for key in request.POST.keys()):
            new_diet = {day: request.POST.get(f'diet_{day}', '') for day in days}
            new_workout = {day: request.POST.get(f'workout_{day}', '') for day in days}

            selected_user.diet_plan = new_diet
            selected_user.workout_plan = new_workout
            selected_user.save()

    return render(request, 'trainers/trainer_dashboard.html', {
        'users': users,
        'selected_user': selected_user,
        'days': days,
    })