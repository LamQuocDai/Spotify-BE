from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .services import create_user_service, get_users_service, get_user_service, update_user_service, delete_user_service

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = create_user_service(data)

        return JsonResponse({"message": "create success","Message code": 200, "data": user.to_json()})

def get_users(request):
    if request.method == 'GET':
        users = get_users_service()
        return JsonResponse({"message": "get success","Message code": 200, "data": users})

def get_user(request, user_id):
    if request.method == 'GET':
        user = get_user_service(user_id)
        if user is None:
            return JsonResponse({"message": "user not found","Message code": 404, "data": None})
        return JsonResponse({"message": "get success","Message code": 200, "data": user.to_json()})

def update_user(request, user_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        user = update_user_service(user_id,data)
        return JsonResponse({"message": "update success","Message code": 200, "data": user.to_json()})

def delete_user(request, user_id):
    if request.method == 'DELETE':
        user = get_user_service(user_id)
        if user is None:
            return JsonResponse({"message": "user not found","Message code": 404, "data": None})
        user = delete_user_service(user_id)
        return JsonResponse({"message": "delete success","Message code": 200, "data": user.to_json()})