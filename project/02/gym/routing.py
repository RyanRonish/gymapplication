from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/gym-status/', consumers.GymStatusConsumer.as_asgi()),
]
