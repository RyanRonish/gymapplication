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

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    apartment_number = models.CharField(max_length=10)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()