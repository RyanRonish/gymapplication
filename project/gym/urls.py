"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('gyms/', views.gyms, name='gyms'),
    path('reservations/<int:gym_id>/', views.reservations, name='reservations'),
    path('profile/', views.profile, name='profile'),
    path('gym/<int:gym_id>/', views.gym_detail, name='gym-detail'),
    path('gym/<int:gym_id>/reserve/<str:time_slot>/', views.make_reservation, name='make-reservation'),
    path('reservation-success/', views.reservation_success, name='reservation-success'),
    path('reservation-failure/', views.reservation_failure, name='reservation-failure'),

    path('choose-gym/', views.choose_gym, name='choose_gym'),
    
    # User authentication views
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

