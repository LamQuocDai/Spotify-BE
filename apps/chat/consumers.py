import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat
from apps.users.models import User

# consumers.py
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"] # hoặc truyền qua URL/query string
        self.id_receiver = int(self.scope['url_route']['kwargs']['receiver_id'])
        self.room_group_name = f'chat_{min(self.user.id, int(self.id_receiver))}_{max(self.user.id, int(self.id_receiver))}'

        if self.user.id.is_authenticated:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Save message to database
        await self.save_message(message)

        # Broadcast message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.user.username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    @database_sync_to_async
    def save_message(self, message):
        receiver = User.objects.get(id=self.id_receiver)
        Chat.objects.create(
            user1=self.user,
            user2=receiver,
            message=message,
        )
