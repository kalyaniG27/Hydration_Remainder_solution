from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    
    daily_goal = models.PositiveIntegerField(default=2000)  # in ml
    reminder_interval = models.PositiveIntegerField(default=0)  # in minutes
    last_reminder_sent = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"
class WaterIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()  # in ml
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
   

    def __str__(self):
        return f"{self.user.username} - {self.amount}ml on {self.date}"
    
class ReminderTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reminder_times")
    time = models.TimeField()

    def __str__(self):
        return f"{self.user.username} - {self.time}"    

class WaterEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()  # in ml
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount}ml at {self.time}"    