from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from datetime import date
from .utils import generate_diet_prompt, generate_workout_prompt, call_groq_api, parse_diet_response

import re

def parse_workout_response(response):
    """Parses a markdown-style workout plan into a dictionary."""
    lines = response.splitlines()
    table_started = False
    headers = []
    workout_table = {}

    for line in lines:
        line = line.strip()
        if not line or line.startswith("**"):
            continue

        if line.startswith("| Day "):
            table_started = True
            continue

        if table_started and line.startswith("|"):
            parts = [p.strip() for p in line.strip('|').split('|')]
            if len(parts) == 5 and parts[0] != 'Day':
                day = parts[0]
                workout_table[day] = {
                    "warmup": parts[1],
                    "strength": parts[2],
                    "cardio": parts[3],
                    "cooldown": parts[4],
                }

    return workout_table

@login_required
def profile_create(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile_detail', pk=profile.pk)
    else:
        form = UserProfileForm()
    return render(request, 'profile_form.html', {'form': form})


@login_required
def profile_update(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save()

            # Regenerate diet plan
            diet_prompt = generate_diet_prompt(profile)
            diet_response = call_groq_api(diet_prompt)
            profile.diet_plan = parse_diet_response(diet_response)

            # Regenerate workout plan
            workout_prompt = generate_workout_prompt(profile)
            workout_response = call_groq_api(workout_prompt)
            profile.workout_plan = parse_workout_response(workout_response)

            profile.save()
            return redirect('profile_detail', pk=profile.pk)
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'profile_form.html', {'form': form})


@login_required
def profile_detail(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk, user=request.user)

    def calculate_age(dob):
        today = date.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    def calculate_bmi(weight, height):
        if height > 0:
            height_m = height / 100
            return round(weight / (height_m ** 2), 2)
        return None

    age = calculate_age(profile.date_of_birth)
    bmi = calculate_bmi(profile.weight, profile.height)

    context = {
        'profile': profile,
        'age': age,
        'bmi': bmi,
    }

    return render(request, 'profile_detail.html', context)

@login_required
def generate_diet_plan(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk, user=request.user)

    if 'regenerate' in request.GET or not profile.diet_plan:
        prompt = generate_diet_prompt(profile)
        response = call_groq_api(prompt)
        print("Groq diet response:", response)
        try:
            diet_table = parse_diet_response(response)
            profile.diet_plan = diet_table
            profile.save()
        except Exception as e:
            print("Failed to parse Groq diet response:", e)
            diet_table = {}
    else:
        diet_table = profile.diet_plan

    diet_notes = [
        "Eat at least 5 servings of fruits and vegetables daily.",
        "Incorporate lean protein sources like chicken, fish, and legumes.",
        "Choose whole grains like brown rice, quinoa, and whole wheat bread.",
        "Drink at least 8-10 glasses of water daily.",
        "Avoid processed and packaged foods.",
        "Cook meals at home using healthy oils and spices."
    ]

    return render(request, 'userprofile/diet_plan.html', {
        'diet_table': diet_table,
        'diet_notes': diet_notes,
        'profile': profile,
    })

@login_required
def generate_workout_plan(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk, user=request.user)

    if 'regenerate' in request.GET or not profile.workout_plan:
        prompt = generate_workout_prompt(profile)
        response = call_groq_api(prompt)
        print("Groq workout response:", response)
        try:
            workout_table = parse_workout_response(response)
            profile.workout_plan = workout_table
            profile.save()
        except Exception as e:
            print("Failed to parse Groq workout response:", e)
            workout_table = {}
    else:
        workout_table = profile.workout_plan

    workout_notes = [
        "Warm-up and cool-down exercises can be adjusted based on preferences and comfort.",
        "Start light and progress slowly to prevent injury.",
        "Cardio intensity can be increased as fitness improves.",
        "Listen to your body and rest as needed."
    ]

    return render(request, 'userprofile/workout_plan.html', {
        'workout_table': workout_table,
        'workout_notes': workout_notes,
        'profile': profile,
    })