from django.shortcuts import render, redirect
from .forms import SignupForm, CustomLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from .models import WaterIntake, UserProfile
import calendar
from collections import defaultdict
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from django.db import models
from django.core.mail import send_mail
from django.conf import settings

class UserLoginView(LoginView):
    template_name = 'tracker/login.html'
    authentication_form = CustomLoginForm

def logout_view(request):
    logout(request)
    return redirect('tracker:login')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(username=email).exists():
                messages.error(request, "An account with this email already exists.")
            else:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                )
                login(request, user)
                send_reminder_email(user.email)  # Send reminder email after signup
                return redirect('tracker:dashboard')
    else:
        form = SignupForm()
    return render(request, 'tracker/signup.html', {'form': form})

@login_required
def home(request):
    daily_goal = 2000  # or get from user profile
    today = timezone.now().date()
    if request.method == "POST":
        amount = int(request.POST.get("amount", 0))
        if amount > 0:
            WaterIntake.objects.create(
                user=request.user,
                amount=amount,
                date=today,
                time=timezone.now().time()
            )
            return redirect('tracker:home')
    current_intake = WaterIntake.objects.filter(user=request.user, date=today).aggregate(Sum('amount'))['amount__sum'] or 0
    progress_percent = int((current_intake / daily_goal) * 100) if daily_goal > 0 else 0
    todays_entries = WaterIntake.objects.filter(user=request.user, date=today).order_by('-time')
    context = {
        'daily_goal': daily_goal,
        'current_intake': current_intake,
        'progress_percent': progress_percent,
        'todays_entries': todays_entries,
    }
    return render(request, 'tracker/home.html', context)

@login_required
def dashboard_view(request):
    today = timezone.now().date()
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if not hasattr(profile, 'daily_goal') or not profile.daily_goal:
        profile.daily_goal = 2000  # default
        profile.save()
    daily_goal = profile.daily_goal

    reminder_message = ""
    if request.method == "POST":
        if "set_goal" in request.POST:
            goal = int(request.POST.get("goal", 2000))
            profile.daily_goal = goal
            profile.save()
            daily_goal = goal
            send_reminder_email(request.user.email)  # Send reminder email when goal is set
        if "add_water" in request.POST:
            amount = int(request.POST.get("amount", 0))
            if amount > 0:
                WaterIntake.objects.create(
                    user=request.user,
                    amount=amount,
                    date=today,
                    time=timezone.now().time()
                )
                return redirect('tracker:dashboard')
        if "set_reminder" in request.POST:
            interval = int(request.POST.get("reminder_interval"))
            profile.reminder_interval = interval
            profile.save()
            reminder_message = f"Reminder set for every {interval} minutes!"

    current_intake = WaterIntake.objects.filter(user=request.user, date=today).aggregate(models.Sum('amount'))['amount__sum'] or 0
    progress_percent = int((current_intake / daily_goal) * 100) if daily_goal > 0 else 0
    todays_entries = WaterIntake.objects.filter(user=request.user, date=today).order_by('-time')

    context = {
        'daily_goal': daily_goal,
        'current_intake': current_intake,
        'progress_percent': progress_percent,
        'todays_entries': todays_entries,
        'reminder_interval': profile.reminder_interval,
        'reminder_message': reminder_message,
    }
    return render(request, 'tracker/dashboard.html', context)

@login_required
def history_view(request):
    from datetime import date

    today = date.today()
    entries = WaterIntake.objects.filter(
        user=request.user,
        date__year=today.year,
        date__month=today.month
    )

    daily_totals = defaultdict(int)
    for entry in entries:
        daily_totals[entry.date.day] += entry.amount

    days_in_month = calendar.monthrange(today.year, today.month)[1]

    history_data = [
        {'day': day, 'total': daily_totals.get(day, 0)}
        for day in range(1, days_in_month + 1)
    ]

    context = {
        'history_data': history_data,
        'month': today.month,
        'year': today.year,
    }
    return render(request, 'tracker/history.html', context)

@login_required
def profile_view(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    reminder_interval = profile.reminder_interval if profile else None
    return render(request, 'tracker/profile.html', {
        'username': request.user.username,
        'email': request.user.email,
        'name': f"{request.user.first_name} {request.user.last_name}",
        'reminder_interval': reminder_interval,
    })

def send_reminder_email(email):
    subject = "Water Intake Reminder"
    message = "Don't forget to set your water intake goal for the day!"
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [email])