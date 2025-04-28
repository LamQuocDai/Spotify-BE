import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat
from apps.users.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        headers = dict(self.scope['headers'])
        auth_header = headers.get(b'authorization', b'').decode('utf-8')

        self.other_user_id = self.scope['url_route']['kwargs']['other_user_id']

        if not self.other_user_id:
            await self.close(code=4000)
            return

        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                # Wrap JWT authentication in database_sync_to_async
                validated_token = await database_sync_to_async(self.get_validated_token)(token)
                self.user = await database_sync_to_async(self.get_user)(validated_token)


                self.other_user = await database_sync_to_async(User.objects.get)(id=self.other_user_id)

                user_id_str = str(self.user.id)
                other_user_id_str = str(self.other_user.id)

                # Create a unique room name based on user IDs
                self.room_group_name = f'chat_{min(self.user.id, self.other_user.id)}_{max(self.user.id, self.other_user.id)}'

                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                await self.accept()
            except AuthenticationFailed:
                await self.close()
        else:
            await self.close()

    def get_validated_token(self, token):
        # This runs in a synchronous context
        return JWTAuthentication().get_validated_token(token)

    def get_user(self, validated_token):
        # This runs in a synchronous context
        return JWTAuthentication().get_user(validated_token)

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await database_sync_to_async(Chat.objects.create)(
            user1=self.user,
            user2=self.other_user,
            message=message
        )

        sender_id = str(self.user.id)
        recipient_id = str(self.other_user.id)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_id,
                'recipient': recipient_id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        recipient = event['recipient']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'recipient': recipient
        }))