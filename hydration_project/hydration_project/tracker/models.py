from django.db import models
from django.contrib.auth.models import User

class WaterIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.user.username} - {self.amount}ml on {self.date}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    daily_goal = models.PositiveIntegerField(default=2000)
    reminder_interval = models.PositiveIntegerField(default=30)  # in minutes
    reminder_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"