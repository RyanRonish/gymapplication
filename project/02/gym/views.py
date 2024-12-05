from datetime import timedelta
from django.contrib.auth import login, decorators
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from .models import Gym, Reservation
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

@login_required
def home(request):
    gym1, _ = Gym.objects.get_or_create(name='Gym 1')
    gym2, _ = Gym.objects.get_or_create(name='Gym 2')
    current_time = timezone.now()

    gym1_is_open = not Reservation.objects.filter(
        gym=gym1,
        time_slot__lte=current_time,
        time_slot__gt=current_time - timedelta(minutes=20)
    ).exists()

    gym2_is_open = not Reservation.objects.filter(
        gym=gym2,
        time_slot__lte=current_time,
        time_slot__gt=current_time - timedelta(minutes=20)
    ).exists()

    return render(request, 'gym_reservation/home.html', {
        'gym1_is_open': gym1_is_open,
        'gym2_is_open': gym2_is_open,
        'gym1': gym1,
        'gym2': gym2,
    })

@login_required
def gyms(request):
    gyms = Gym.objects.all()
    return render(request, 'gym_reservation/gyms.html', {'gyms': gyms})

@login_required
def choose_gym(request):
    gyms = Gym.objects.all()
    return render(request, 'gym_reservation/choose_gym.html', {'gyms': gyms})


@login_required
def gym_detail(request, gym_id):
    gym = get_object_or_404(Gym, id=gym_id)
    current_time = timezone.now().replace(second=0, microsecond=0)
    minutes_to_add = (20 - current_time.minute % 20) % 20
    current_time += timedelta(minutes=minutes_to_add)

    available_slots = [
        current_time + timedelta(minutes=20 * i)
        for i in range(72)  # 72 slots for 24 hours
        if not Reservation.objects.filter(gym=gym, time_slot=current_time + timedelta(minutes=20 * i)).exists()
    ]

    return render(request, 'gym_reservation/gym_detail.html', {
        'gym': gym,
        'available_slots': available_slots
    })

@login_required
def reservations(request, gym_id):
    gym = get_object_or_404(Gym, id=gym_id)
    current_time = timezone.now().replace(second=0, microsecond=0)
    minutes_to_add = (20 - current_time.minute % 20) % 20
    current_time += timedelta(minutes=minutes_to_add)

    am_slots, pm_slots = [], []

    for i in range(72):
        slot_time = current_time + timedelta(minutes=20 * i)
        if not Reservation.objects.filter(gym=gym, time_slot=slot_time).exists():
            (am_slots if slot_time.hour < 12 else pm_slots).append(slot_time)

    user_reservations = Reservation.objects.filter(gym=gym, resident=request.user)

    return render(request, 'gym_reservation/reservations.html', {
        'gym': gym,
        'am_slots': am_slots,
        'pm_slots': pm_slots,
        'reservations': user_reservations
    })

@login_required
def make_reservation(request, gym_id, time_slot):
    gym = get_object_or_404(Gym, id=gym_id)
    time_slot = parse_datetime(time_slot)

    if time_slot is None or Reservation.objects.filter(gym=gym, time_slot=time_slot).exists():
        return redirect('reservation-failure')

    Reservation.objects.create(resident=request.user, gym=gym, time_slot=time_slot)
    return redirect('reservation-success')

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, resident=request.user)
    reservation.delete()
    return redirect('reservations', gym_id=reservation.gym.id)

@login_required
def make_reservation(request, gym_id, time_slot):
    gym = get_object_or_404(Gym, id=gym_id)
    time_slot = parse_datetime(time_slot)

    if time_slot is None or Reservation.objects.filter(gym=gym, time_slot=time_slot).exists():
        return redirect('reservation-failure')

    Reservation.objects.create(resident=request.user, gym=gym, time_slot=time_slot)
    return redirect('reservation-success')


def reservation_success(request):
    return render(request, 'gym_reservation/reservation_success.html')


def reservation_failure(request):
    return render(request, 'gym_reservation/reservation_failure.html')

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, resident=request.user)
    reservation.delete()
    return redirect('reservations', gym_id=reservation.gym.id)

@require_http_methods(["POST"])
def start_workout(request, gym_id):
    gym = Gym.objects.get(id=gym_id)
    gym.is_occupied = True
    gym.save()
    return JsonResponse({'status': 'success', 'gym_open': False})

@require_http_methods(["POST"])
def end_workout(request, gym_id):
    gym = Gym.objects.get(id=gym_id)
    gym.is_occupied = False
    gym.save()
    return JsonResponse({'status': 'success', 'gym_open': True})

@require_http_methods(["GET"])
def get_gym_status(request, gym_id):
    gym = Gym.objects.get(id=gym_id)
    return JsonResponse({'status': 'success', 'gym_open': not gym.is_occupied})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.apartment_number = form.cleaned_data.get('apartment_number')
            user.profile.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

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
