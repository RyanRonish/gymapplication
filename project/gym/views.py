from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from datetime import timedelta, datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Gym, Reservation
from .forms import CustomUserCreationForm, ProfileForm

# Home view - accessible only by logged-in users
@login_required
def home(request):
    # Check if Gym 1 and Gym 2 are open or reserved
    current_time = timezone.now()
    
    gym1_is_open = not Reservation.objects.filter(gym__name='Gym 1', time_slot__gte=current_time).exists()
    gym2_is_open = not Reservation.objects.filter(gym__name='Gym 2', time_slot__gte=current_time).exists()
    
    gym1 = Gym.objects.get(name='Gym 1')
    gym2 = Gym.objects.get(name='Gym 2')
    
    context = {
        'gym1_is_open': gym1_is_open,
        'gym2_is_open': gym2_is_open,
        'gym1': gym1,
        'gym2': gym2,
    }
    
    return render(request, 'gym_reservation/home.html', context)

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

# View to show the user's reservations and handle calendar time slot selection
@login_required
def reservations(request, gym_id):
    gym = Gym.objects.get(id=gym_id)
    reservations = Reservation.objects.filter(gym=gym, resident=request.user)
    
    return render(request, 'gym_reservation/reservations.html', {'reservations': reservations, 'gym': gym})


# Profile view for the logged-in user
@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'gym_reservation/profile.html', {
        'form': form,
        'user': request.user
    })

# View to list all gyms
@login_required
def gyms(request):
    gyms = Gym.objects.all()
    return render(request, 'gym_reservation/gyms.html', {'gyms': gyms})

# User registration view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create the user's profile with apartment number
            user.profile.apartment_number = form.cleaned_data.get('apartment_number')
            user.profile.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def choose_gym(request):
    gyms = Gym.objects.all()
    return render(request, 'gym_reservation/choose_gym.html', {'gyms': gyms})

