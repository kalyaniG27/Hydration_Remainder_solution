from django.shortcuts import render, redirect
from .forms import SignupForm, CustomLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

class UserLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomLoginForm

def home(request):
    daily_goal = 2000
    current_intake = 500
    progress_percent = int((current_intake / daily_goal) * 100) if daily_goal > 0 else 0
    context = {
        'daily_goal': daily_goal,
        'current_intake': current_intake,
        'progress_percent': progress_percent,
    }
    return render(request, 'home.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.cleaned_data.pop('confirm_password')
            form.save()
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def dashboard_view(request):
    daily_goal = 2000
    current_intake = 500
    progress_percent = int((current_intake / daily_goal) * 100) if daily_goal > 0 else 0
    context = {
        'daily_goal': daily_goal,
        'current_intake': current_intake,
        'progress_percent': progress_percent,
    }
    return render(request, 'dashboard.html', context)

@login_required
def history_view(request):
    return render(request, 'history.html')

@login_required
def profile_view(request):
    return render(request, 'profile.html', {
        'username': request.user.username,
        'email': request.user.email,
        'name': f"{request.user.first_name} {request.user.last_name}"
    })