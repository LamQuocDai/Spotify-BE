from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer
import json
from django.views.decorators.csrf import csrf_exempt
from .services import create_user_service, get_users_service, get_user_service, update_user_service, delete_user_service
from apps.utils.response import success_response, error_response
from django.core.serializers import serialize
from rest_framework.permissions import AllowAny
# apps/users/views.py
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

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

            user_json = json.loads(serialize('json', [user]))[0]['fields']
            if user is None:
                return error_response("User doesn't exist")
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
            user = delete_user_service(user_id)
            user_json = json.loads(serialize('json', [user]))[0]['fields']
            return success_response("Delete user success",user_json)
        except Exception as e:
            return error_response(e.__str__())
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if user is None:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
