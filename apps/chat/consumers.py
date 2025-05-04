import json
import urllib.parse
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat
from apps.users.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract token from query string
        query_string = self.scope['query_string'].decode('utf-8')
        query_params = dict(urllib.parse.parse_qsl(query_string))
        token = query_params.get('token')

        if not token:
            # If no token in query params, check headers
            headers = dict(self.scope['headers'])
            auth_header = headers.get(b'authorization', b'').decode('utf-8')
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            # No authentication provided, reject the connection
            await self.close(code=4001)
            return

        # Authenticate the user
        try:
            # Use synchronous JWT authentication in an async context
            validated_token = await database_sync_to_async(self.get_validated_token)(token)
            self.user = await database_sync_to_async(self.get_user)(validated_token)

            # Get other user information
            self.other_user_id = self.scope['url_route']['kwargs']['other_user_id']
            self.other_user = await database_sync_to_async(User.objects.get)(id=self.other_user_id)

            # Create a chat room name based on user IDs (ordered to ensure consistency)
            self.room_group_name = f'chat_{min(str(self.user.id), str(self.other_user.id))}_{max(str(self.user.id), str(self.other_user.id))}'

            # Add this connection to the group
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

            # Accept the connection
            await self.accept()

            # Send authentication success message
            await self.send(text_data=json.dumps({
                'type': 'authentication_success'
            }))

        except (AuthenticationFailed, User.DoesNotExist) as e:
            # Authentication failed or user not found
            error_message = "Authentication failed" if isinstance(e, AuthenticationFailed) else "User not found"
            await self.close(code=4003)

    def get_validated_token(self, token):
        # Synchronous method to validate the token
        return JWTAuthentication().get_validated_token(token)

    def get_user(self, validated_token):
        # Synchronous method to get the user from token
        return JWTAuthentication().get_user(validated_token)

    async def disconnect(self, close_code):
        # Remove from group on disconnect
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)

            # Handle ping messages for keeping the connection alive
            if text_data_json.get('type') == 'ping':
                await self.send(text_data=json.dumps({
                    'type': 'pong'
                }))
                return

            # Handle regular chat messages
            if 'message' in text_data_json:
                message = text_data_json['message']

                # Save message to database
                await database_sync_to_async(Chat.objects.create)(
                    user1=self.user,
                    user2=self.other_user,
                    message=message
                )

                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'sender': str(self.user.id),
                        'recipient': str(self.other_user.id)
                    }
                )
        except json.JSONDecodeError:
            # Handle invalid JSON
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))
        except Exception as e:
            # Handle other exceptions
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'Error processing message: {str(e)}'
            }))

    async def chat_message(self, event):
        # Send message to WebSocket
        message = event['message']
        sender = event['sender']
        recipient = event['recipient']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'recipient': recipient
        }))