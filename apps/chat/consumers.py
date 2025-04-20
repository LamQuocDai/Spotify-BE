import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .schemas import PrivateMessageIn
from . import services

# consumers.py
class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.id_sender = self.scope["user"].id  # hoặc truyền qua URL/query string
        self.id_receiver = int(self.scope['url_route']['kwargs']['receiver_id'])
        self.group_name = services.get_private_group_service(self.id_sender, self.id_receiver)

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
