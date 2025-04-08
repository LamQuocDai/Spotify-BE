from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
import json
from apps.utils.response import success_response, error_response
from .services import create_chat_service, get_chats_service, get_chat_service, update_chat_service, delete_chat_service

@csrf_exempt
def create_chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            chat = create_chat_service(data)
            chat_json = json.loads(serialize('json', [chat]))[0]['fields']

            return success_response("Create chat success",chat_json)
        except Exception as e:
            return error_response(e.__str__())


def get_chats(request):
    if request.method == 'GET':
        try:
            chats = get_chats_service()
            return success_response("Get list success",chats)
        except Exception as e:
            return error_response(e.__str__())

def get_chat(request, chat_id):
    if request.method == 'GET':
        try:
            chat = get_chat_service(chat_id)

            if chat is None:
                return error_response("Chat doesn't exist")
            chat_json = json.loads(serialize('json', [chat]))[0]['fields']
            return success_response("Get chat success",chat_json)
        except Exception as e:
            return error_response(e.__str__())

@csrf_exempt
def update_chat(request, chat_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            chat = update_chat_service(chat_id,data)
            if chat is None:
                return error_response("Chat doesn't exist")
            chat_json = json.loads(serialize('json', [chat]))[0]['fields']
            return success_response("Update chat success",chat_json)
        except Exception as e:
            return error_response(e.__str__())

@csrf_exempt
def delete_chat(request, chat_id):
    if request.method == 'DELETE':
        try:
            chat = get_chat_service(chat_id)
            if chat is None:
                return error_response("Chat doesn't exist")
            chat_delete = delete_chat_service(chat_id)
            chat_json = json.loads(serialize('json', [chat_delete]))[0]['fields']
            return success_response("Delete chat success",chat_json)
        except Exception as e:
            return error_response(e.__str__())