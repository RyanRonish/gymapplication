from django.urls import path
from .consumers import GymConsumer

websocket_urlpatterns = [
    path('ws/gym-status/', GymConsumer.as_asgi()),
]
