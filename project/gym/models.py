from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Gym(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    resident = models.ForeignKey(User, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    time_slot = models.DateTimeField()
    duration = models.IntegerField(default=20)  # 20-minute slots

    def __str__(self):
        return f'{self.resident.username} - {self.gym.name} at {self.time_slot}'
    
    class Meta:
        unique_together = ('gym', 'time_slot')  # Prevent overlapping reservations
