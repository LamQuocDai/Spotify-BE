from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Chat
from .schemas import PrivateMessageIn

def create_chat_service(data):
    try:
        chat = Chat.objects.create(
            user1_id=data['user1_id'],
            user2_id=data['user2_id'],
            message=data['message'],
        )
        return chat
    except Exception as e:
        return None

def get_chats_service():
    return list(Chat.objects.all().values())

def get_chat_service(chat_id):
    try:
        chat = Chat.objects.get(id=chat_id)
        return chat
    except Chat.DoesNotExist:
        return None
    except Chat.MultipleObjectsReturned:
        return None

def update_chat_service(chat_id, data):
    try:
        chat = Chat.objects.get(id=chat_id)
        chat.message = data.get('message', chat.message)

        chat.save()
        return chat
    except Chat.DoesNotExist:
        return None
    except Chat.MultipleObjectsReturned:
        return None

def delete_chat_service(chat_id):
    try:
        chat = Chat.objects.get(id=chat_id)
        chat.delete()
        return chat
    except Chat.DoesNotExist:
        return None
    except Chat.MultipleObjectsReturned:
        return None

def get_private_group_service(id_sender, id_receiver):
    return f"chat{min(id_sender, id_receiver)}_{max(id_sender, id_receiver)}"

def save_message_service(data: PrivateMessageIn):
    try:
        return Chat.objects.create(
            user1_id=data.user1_id,
            user2_id=data.user2_id,
            message=data.message,
        )
    except Exception as e:
        return None

def broadcast_private_message_service(data: PrivateMessageIn):
    try:
        group = get_private_group_service(data.user1_id, data.user2_id)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(group, {
            'type': 'chat_message',
            'message': data.message,
            'user1_id': data.user1_id,
            'user2_id': data.user2_id,
        })
    except Exception as e:
        return None