from celery import shared_task
from django.utils.timezone import now, timedelta
from django.core.mail import send_mail
from tracker.models import UserProfile
from django.conf import settings

@shared_task
def send_hydration_reminders():
    users = UserProfile.objects.all()
    for user in users:
        if user.email and now() >= user.next_reminder_time:
            try:
                send_mail(
                    subject="💧 Hydration Reminder",
                    message=f"Hi {user.user.username}, it's time to drink water and stay hydrated!",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                print(f"✅ Reminder sent to {user.email}")

                # Update next reminder time
                user.next_reminder_time = now() + timedelta(minutes=user.reminder_interval_minutes)
                user.save()
            except Exception as e:
                print(f"❌ Failed to send reminder to {user.email}: {e}")
