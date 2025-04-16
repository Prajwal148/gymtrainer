from django import forms
from userprofile.models import UserProfile

class DietPlanForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['diet_plan']
class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['workout_plan']