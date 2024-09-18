from django.shortcuts import render
from .models import Gym
from django.utils import timezone
from .models import Reservation, Gym
from datetime import timedelta
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime

def home(request):
    gyms = Gym.objects.all()
    return render(request, 'gym_reservation/home.html', {'gyms': gyms})

def gym_detail(request, gym_id):
    gym = Gym.objects.get(id=gym_id)
    current_time = timezone.now()
    available_slots = []

    # Generate 20-minute time slots for the next 24 hours
    for i in range(72):  # 72 slots of 20 minutes in 24 hours
        slot_time = current_time + timedelta(minutes=20 * i)
        if not Reservation.objects.filter(gym=gym, time_slot=slot_time).exists():
            available_slots.append(slot_time)

    return render(request, 'gym_reservation/gym_detail.html', {
        'gym': gym,
        'available_slots': available_slots
    })

@login_required
def make_reservation(request, gym_id, time_slot):
    gym = Gym.objects.get(id=gym_id)
    time_slot = parse_datetime(time_slot)  # Automatically parses the time string
    
    # If the time slot is invalid or cannot be parsed, return an error
    if time_slot is None:
        return redirect('reservation-failure')
    
    # Check if the time slot is available
    if not Reservation.objects.filter(gym=gym, time_slot=time_slot).exists():
        reservation = Reservation(resident=request.user, gym=gym, time_slot=time_slot)
        reservation.save()
        return redirect('reservation-success')
    
    return redirect('reservation-failure')

def reservation_success(request):
    return render(request, 'gym_reservation/reservation_success.html')

def reservation_failure(request):
    return render(request, 'gym_reservation/reservation_failure.html')