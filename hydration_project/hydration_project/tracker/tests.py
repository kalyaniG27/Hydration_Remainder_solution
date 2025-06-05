from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

def send_water_intake_reminder(user: User):
    subject = "Reminder to Set Your Water Intake"
    message = "Hi {},\n\nDon't forget to set your water intake for today! Stay hydrated!".format(user.first_name)
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)