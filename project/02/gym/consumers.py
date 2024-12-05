import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Gym

class GymConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add the WebSocket connection to the group
        await self.channel_layer.group_add("gym_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the WebSocket connection from the group
        await self.channel_layer.group_discard("gym_updates", self.channel_name)

    async def receive(self, text_data):
        # Parse incoming data
        data = json.loads(text_data)
        gym_id = data['gym_id']
        status = data['status']  # "open" or "occupied"

        # Update the database
        await self.update_gym_status(gym_id, status)

        # Send the update to all users in the group
        await self.channel_layer.group_send(
            "gym_updates",
            {
                'type': 'gym_status_update',
                'gym_id': gym_id,
                'status': status,
            }
        )

    async def gym_status_update(self, event):
        # Send the update to the WebSocket client
        await self.send(text_data=json.dumps({
            'gym_id': event['gym_id'],
            'status': event['status'],
        }))

    @sync_to_async
    def update_gym_status(self, gym_id, status):
        # Update the database to reflect the gym's status
        gym = Gym.objects.get(id=gym_id)
        gym.is_open = (status == 'open')
        gym.save()

# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class GymStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("gym_status", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("gym_status", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            "gym_status",
            {
                "type": "update_status",
                "message": data["message"],
            },
        )

    async def update_status(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))
