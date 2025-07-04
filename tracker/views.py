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

from django.db.models import Sum
from django.db import models
from datetime import timedelta, date
from django.http import JsonResponse
from .models import WaterEntry
from django.utils import timezone

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
            if User.objects.filter(email=email).exists():
                messages.error(request, "An account with this email already exists.")
            else:
                user = User.objects.create_user(
                    username=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password']
                )
                profile, created = UserProfile.objects.get_or_create(user=user)
                profile.daily_goal = form.cleaned_data.get('daily_goal', 2000)
                profile.reminder_interval = form.cleaned_data.get('reminder_interval', 0)
                profile.save()

                messages.success(request, "Account created successfully! Please log in.")
                return redirect('tracker:login')
    else:
        form = SignupForm()
    return render(request, 'tracker/signup.html', {'form': form})

@login_required
def home(request):
    profile = UserProfile.objects.get(user=request.user)
    daily_goal = profile.daily_goal
    today = timezone.localtime(timezone.now()).date()
    if request.method == "POST":
        amount = int(request.POST.get("amount", 0))
        if amount > 0:
            WaterIntake.objects.create(
                user=request.user,
                amount=amount,
                date=today,
                time=timezone.localtime(timezone.now()).time()
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
    today = timezone.localtime(timezone.now()).date()
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if not profile.daily_goal:
        profile.daily_goal = 2000
        profile.save()

    daily_goal = profile.daily_goal
    reminder_message = ""

    if request.method == "POST":
        if "set_goal" in request.POST:
            goal = int(request.POST.get("goal", 2000))
            profile.daily_goal = goal
            profile.save()
            daily_goal = goal
        if "add_water" in request.POST:
            amount = int(request.POST.get("amount", 0))
            if amount > 0:
                WaterIntake.objects.create(
                    user=request.user,
                    amount=amount,
                    date=today,
                    time=timezone.localtime(timezone.now()).time()
                )
                return redirect('tracker:dashboard')
        if "set_reminder" in request.POST:
            interval = int(request.POST.get("reminder_interval"))
            profile.reminder_interval = interval
            profile.save()
            reminder_message = f"Reminder set for every {interval} minutes!"

    current_intake = WaterIntake.objects.filter(user=request.user, date=today).aggregate(Sum('amount'))['amount__sum'] or 0
    progress_percent = int((current_intake / daily_goal) * 100) if daily_goal > 0 else 0
    todays_entries = WaterIntake.objects.filter(user=request.user, date=today).order_by('-time')

    show_reminder_popup = False
    popup_message = ""
    now = timezone.now()
    if profile.reminder_interval > 0:
        if not profile.last_reminder_sent:
            show_reminder_popup = True
            popup_message = "💧 Time to drink water! (Popup Reminder)"
            profile.last_reminder_sent = now
            profile.save()
            send_mail(
                subject="💧 Time to Hydrate!",
                message=f"Hi {request.user.first_name}, don't forget to drink water!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=True,
            )
        else:
            seconds_since_last = (now - profile.last_reminder_sent).total_seconds()
            if seconds_since_last >= profile.reminder_interval * 60:
                show_reminder_popup = True
                popup_message = "💧 Time to drink water! (Popup Reminder)"
                profile.last_reminder_sent = now
                profile.save()
                send_mail(
                    subject="💧 Time to Hydrate!",
                    message=f"Hi {request.user.first_name}, don't forget to drink water!",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[request.user.email],
                    fail_silently=True,
                )

    streak = 0
    day = today
    while True:
        total = WaterIntake.objects.filter(user=request.user, date=day).aggregate(Sum('amount'))['amount__sum'] or 0
        if total >= daily_goal:
            streak += 1
            day -= timedelta(days=1)
        else:
            break
    profile.streak = streak
    profile.save()
    context = {
        'daily_goal': daily_goal,
        'current_intake': current_intake,
        'progress_percent': progress_percent,
        'todays_entries': todays_entries,
        'reminder_interval': profile.reminder_interval,
        'reminder_message': reminder_message,
        'show_reminder_popup': show_reminder_popup,
        'popup_message': popup_message,
        'current_streak': streak,
    }
    return render(request, 'tracker/dashboard.html', context)

@login_required
def history_view(request):
    today = timezone.localtime(timezone.now()).date()
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

@login_required
def check_reminder_due(request):
    profile = UserProfile.objects.get(user=request.user)
    now = timezone.now()
    is_due = False
    if profile.reminder_interval > 0:
        if not profile.last_reminder_sent or (now - profile.last_reminder_sent).total_seconds() >= profile.reminder_interval * 60:
            is_due = True
            profile.last_reminder_sent = now
            profile.save()
            send_mail(
                subject="💧 Time to Hydrate!",
                message=f"Hi {request.user.first_name}, don't forget to drink water!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=False,
            )
    return JsonResponse({"reminder": is_due})

def test_email(request):
    send_mail(
        "Test Email",
        "This is a test email from Django.",
        settings.DEFAULT_FROM_EMAIL,
        ['kggarud27@gmail.com'],
        fail_silently=False,
    )
    return JsonResponse({"status": "sent"})

def test_email_view(request):
    try:
        send_mail(
            subject='Test Email',
            message='This is a test email from Django.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        return JsonResponse({'status': 'sent'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
