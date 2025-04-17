from django import forms
from userprofile.models import UserProfile
from .models import Trainer

class DietPlanForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['diet_plan']
class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['workout_plan']

class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['Firstname', 'Lastname', 'specialization', 'bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }