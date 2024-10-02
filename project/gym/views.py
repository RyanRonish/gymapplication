from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from .models import Gym, Reservation

# Home view - accessible only by logged-in users
@login_required
def home(request):
    gyms = Gym.objects.all()
    return render(request, 'gym_reservation/home.html', {'gyms': gyms})

# Gym detail view - accessible only by logged-in users
@login_required
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

# View to handle making a reservation
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

# Success and failure views for reservation outcomes
def reservation_success(request):
    return render(request, 'gym_reservation/reservation_success.html')

def reservation_failure(request):
    return render(request, 'gym_reservation/reservation_failure.html')

# View to show the user's reservations
@login_required
def reservations(request):
    reservations = Reservation.objects.filter(resident=request.user)
    return render(request, 'gym_reservation/reservations.html', {'reservations': reservations})

# Profile view for the logged-in user
@login_required
def profile(request):
    user = request.user
    return render(request, 'gym_reservation/profile.html', {'user': user})

# View to list all gyms
@login_required
def gyms(request):
    gyms = Gym.objects.all()
    return render(request, 'gym_reservation/gyms.html', {'gyms': gyms})

# User registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after successful registration
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})
