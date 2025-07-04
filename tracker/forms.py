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
    email = forms.EmailField(required=True)
    
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Create a password',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm your password',
    }))
    


    class Meta:
        model = UserProfile  # Use UserProfile, not User
        fields = [
            'first_name', 'last_name', 'email', 'password',
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