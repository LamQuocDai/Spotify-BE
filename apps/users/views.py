from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
import json
from apps.utils.response import success_response, error_response
from .services import create_user_service, get_users_service, get_user_service, update_user_service, delete_user_service

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = create_user_service(data)
            user_json = json.loads(serialize('json', [user]))[0]['fields']

            return success_response("Create user success",user_json)
        except Exception as e:
            return error_response(e.__str__())


def get_users(request):
    if request.method == 'GET':
        try:
            users = get_users_service()
            return success_response("Get list success",users)
        except Exception as e:
            return error_response(e.__str__())

def get_user(request, user_id):
    if request.method == 'GET':
        try:
            user = get_user_service(user_id)

            if user is None:
                return error_response("User doesn't exist")
            user_json = json.loads(serialize('json', [user]))[0]['fields']
            return success_response("Get user success",user_json)
        except Exception as e:
            return error_response(e.__str__())

@csrf_exempt
def update_user(request, user_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            user = update_user_service(user_id,data)
            if user is None:
                return error_response("User doesn't exist")
            user_json = json.loads(serialize('json', [user]))[0]['fields']
            return success_response("Update user success",user_json)
        except Exception as e:
            return error_response(e.__str__())

@csrf_exempt
def delete_user(request, user_id):
    if request.method == 'DELETE':
        try:
            user = get_user_service(user_id)
            if user is None:
                return error_response("User doesn't exist")
            user_delete = delete_user_service(user_id)
            user_json = json.loads(serialize('json', [user_delete]))[0]['fields']
            return success_response("Delete user success",user_json)
        except Exception as e:
            return error_response(e.__str__())