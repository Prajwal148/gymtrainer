from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

class UserCreateForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        (False, 'User'),
        (True, 'Trainer'),
    ]
    is_trainer = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        initial=False,
        required=True,
    )

    class Meta:
        fields = ('is_trainer','username', 'email', 'password1', 'password2')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'User Name'
        self.fields['email'].label = 'Email'
