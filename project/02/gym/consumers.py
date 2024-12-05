from channels.generic.websocket import AsyncWebsocketConsumer
import json

class GymStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("gym_status", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("gym_status", self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        status = text_data_json['status']

        # Send status to group
        await self.channel_layer.group_send(
            "gym_status",
            {
                'type': 'gym_status',
                'status': status
            }
        )

    # Receive message from room group
    async def gym_status(self, event):
        status = event['status']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'status': status
        }))
