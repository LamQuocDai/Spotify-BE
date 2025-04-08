from .models import Chat

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
