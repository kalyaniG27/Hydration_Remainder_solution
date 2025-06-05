from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from .models import UserProfile

@shared_task
def send_water_reminders():
    now = timezone.now()
    profiles = UserProfile.objects.filter(reminder_interval__gt=0)
    for profile in profiles:
        last_sent = profile.last_reminder_sent
        if not last_sent or (now - last_sent).total_seconds() >= profile.reminder_interval * 60:
            if profile.user.email:
                print(f"Sending email to {profile.user.email}")  # Add this line
                send_mail(
                    'Hydration Reminder',
                    'Time to drink water!',
                    'your_gmail@gmail.com',
                    [profile.user.email],
                )
                profile.last_reminder_sent = now
                profile.save()