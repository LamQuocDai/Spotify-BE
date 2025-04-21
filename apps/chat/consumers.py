import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .schemas import PrivateMessageIn
from channels.db import database_sync_to_async
from .models import Chat
from apps.users.models import User

# consumers.py
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.id_sender = self.scope["user"].id  # hoặc truyền qua URL/query string
        self.id_receiver = int(self.scope['url_route']['kwargs']['receiver_id'])
        self.room_group_name = f'chat_{min(self.user.id, int(self.id_))}_{max(self.user.id, int(self.other_user_id))}'

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        msg_in = PrivateMessageIn(**data)
        services.save_message_service(msg_in)
        services.broadcast_private_message_service(msg_in)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
