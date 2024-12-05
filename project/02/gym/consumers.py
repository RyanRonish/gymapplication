import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Gym


class GymConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add the WebSocket to a group for broadcasting gym updates
        await self.channel_layer.group_add("gym_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the WebSocket from the group
        await self.channel_layer.group_discard("gym_updates", self.channel_name)

    async def receive(self, text_data):
        # Parse the incoming data
        data = json.loads(text_data)
        gym_id = data['gym_id']
        status = data['status']

        # Update the database
        await self.update_gym_status(gym_id, status)

        # Broadcast the update to the group
        await self.channel_layer.group_send(
            "gym_updates",
            {
                'type': 'gym_status_update',
                'gym_id': gym_id,
                'status': status,
            }
        )

    async def gym_status_update(self, event):
        # Send the status update to the WebSocket client
        await self.send(text_data=json.dumps({
            'gym_id': event['gym_id'],
            'status': event['status'],
        }))

    @sync_to_async
    def update_gym_status(self, gym_id, status):
        # Retrieve and update the gym status in the database
        gym = Gym.objects.get(id=gym_id)
        gym.is_open = (status == 'open')
        gym.save()
