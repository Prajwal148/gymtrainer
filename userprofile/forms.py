from django import forms
from .models import UserProfile
from datetime import date

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'date_of_birth', 'height', 'weight', 'smoking', 'alcohol', 'food_habits', 'workout_experience']
        widgets = {
            'food_habits': forms.RadioSelect,
            'workout_experience': forms.RadioSelect,
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'dob'}),
        }
        labels = {
            'height': 'Height (CM)',
            'weight': 'Weight (KG)',
        }

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 21:
            raise forms.ValidationError("You must be at least 21 years old to register.")
        return dob
