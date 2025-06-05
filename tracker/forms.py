from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile

class ReminderIntervalForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['reminder_interval']

ACTIVITY_CHOICES = [
    ('Light', 'Light (light exercise 1–3 days/week)'),
    ('Moderate', 'Moderate (3–5 days/week)'),
    ('Intense', 'Intense (daily or heavy training)'),
]

class SignupForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Enter your first name',
    }))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Enter your last name',
    }))
    mobile_no = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your mobile number'})
    )
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Create a password',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm your password',
    }))
    weight = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        'placeholder': 'Enter your weight',
    }))
    location = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'City, Country',
    }))
    activity_level = forms.ChoiceField(choices=ACTIVITY_CHOICES, widget=forms.Select())
    water_goal = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        'value': '2000',
    }))

    class Meta:
        model = UserProfile  # Use UserProfile, not User
        fields = [
            'first_name', 'last_name', 'mobile_no', 'email', 'password',
            'weight', 'location', 'activity_level', 'water_goal'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords do not match.")

class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'your.email@example.com',
        'class': 'form-input'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'form-input'
    }))