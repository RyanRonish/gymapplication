from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.db import models
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from .models import Gym

class GymStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("gym_status", self.channel_name)
        await self.accept()

        # Fetch the initial gym status when the WebSocket connects
        gym = await self.get_gym_status()
        await self.send(text_data=json.dumps({'status': gym.is_occupied}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("gym_status", self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        status = text_data_json['status']

        # Update the gym status in the database
        await self.update_gym_status(status)

        # Send status to group
        await self.channel_layer.group_send(
            "gym_status",
            {
                'type': 'gym_status',
                'status': status
            }
        )

    async def gym_status(self, event):
        status = event['status']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'status': status
        }))

    @database_sync_to_async
    def get_gym_status(self):
        # Assuming you have only one gym record
        gym = Gym.objects.first()
        if gym is None:
            # Initialize the gym record if it does not exist
            gym = Gym.objects.create(name="Default Gym", is_occupied=False)
        return gym

    @database_sync_to_async
    def update_gym_status(self, occupied):
        gym = Gym.objects.first()
        if gym:
            gym.is_occupied = occupied
            gym.save()
