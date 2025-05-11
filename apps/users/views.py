import json
import requests
import uuid
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from social_django.models import UserSocialAuth
import logging
from django.core.cache import cache
from .services import (
    create_user_service,
    get_users_service,
    get_user_service,
    update_user_service,
    delete_user_service,
    search_users_service
)
from Spotify_BE import settings
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer, SocialLoginSerializer, CustomTokenObtainPairSerializer
from .models import User
from apps.utils.response import success_response, error_response
from django.contrib.auth.models import Group

# Set up logging
logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = CustomTokenObtainPairSerializer.get_token(user)

        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if user is None:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = CustomTokenObtainPairSerializer.get_token(user)

        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class SocialLoginView(generics.GenericAPIView):
    serializer_class = SocialLoginSerializer
    permission_classes = [AllowAny]

    TOKEN_URL = "https://oauth2.googleapis.com/token"
    USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error("Serializer errors: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        code = serializer.validated_data['code']
        logger.info("Processing Google login: code=%s", code[:10] + "...")

        cache_key = f"auth_code:{code}"
        if cache.get(cache_key):
            logger.warning("Authorization code already used: %s", code[:10] + "...")
            return Response(
                {'detail': 'Authorization code has already been used'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            logger.info("Requesting access token from: %s", self.TOKEN_URL)
            token_response = requests.post(
                self.TOKEN_URL,
                data={
                    'code': code,
                    'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                    'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
                    'redirect_uri': settings.SOCIAL_AUTH_REDIRECT_URI,
                    'grant_type': 'authorization_code',
                },
                timeout=10
            )
            if token_response.status_code != 200:
                logger.error("Failed to get access token: %s", token_response.text)
                return Response(
                    {'detail': 'Failed to get access token'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            access_token = token_response.json().get('access_token')
            if not access_token:
                logger.error("No access token in response")
                return Response(
                    {'detail': 'No access token returned'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            cache.set(cache_key, True, timeout=60)

            logger.info("Fetching user info from: %s", self.USER_INFO_URL)
            user_response = requests.get(
                self.USER_INFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10
            )
            if user_response.status_code != 200:
                logger.error("Failed to get user info: %s", user_response.text)
                return Response(
                    {'detail': 'Failed to get user info'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            user_data = user_response.json()
            logger.info("User data: %s", {k: v for k, v in user_data.items() if k != 'picture'})

            email = user_data.get('email')
            if not email:
                logger.error("No email provided")
                return Response(
                    {'detail': 'Email not provided by Google'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            name = user_data.get('name', email.split('@')[0])
            picture = user_data.get('picture')
            provider_id = user_data.get('sub')

            with transaction.atomic():
                user, created = User.objects.select_for_update().get_or_create(
                    email=email,
                    defaults={
                        'username': email.split('@')[0][:15],
                        'first_name': name.split()[0] if name and ' ' in name else name,
                        'last_name': ' '.join(name.split()[1:]) if name and ' ' in name else '',
                        'image': picture,
                    }
                )
                if created:
                    user.set_unusable_password()
                    user.save()
                    # Gán người dùng vào nhóm 'user' mặc định
                    user_group, _ = Group.objects.get_or_create(name='user')
                    user.groups.add(user_group)
                    logger.info("Created new user: username=%s, email=%s", user.username, email)
                else:
                    user.first_name = name.split()[0] if name and ' ' in name else name
                    user.last_name = ' '.join(name.split()[1:]) if name and ' ' in name else ''
                    user.image = picture
                    user.save()
                    logger.info("Updated user: username=%s, email=%s", user.username, email)

                if created and User.objects.filter(username=user.username).exclude(id=user.id).exists():
                    user.username = f"{user.username[:10]}_{uuid.uuid4().hex[:4]}"
                    user.save()
                    logger.info("Updated username due to collision: %s", user.username)

                social_auth, social_created = UserSocialAuth.objects.update_or_create(
                    user=user,
                    provider='google',
                    defaults={'uid': provider_id}
                )
                logger.info("Social auth %s: user=%s, uid=%s",
                           "created" if social_created else "updated", user.username, provider_id)

                refresh = CustomTokenObtainPairSerializer.get_token(user)

                logger.info("Returning response for user: %s", user.username)
                return Response({
                    'user': UserSerializer(user).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Authentication error: %s", str(e))
            return Response(
                {'detail': 'Authentication error'},
                status=status.HTTP_401_UNAUTHORIZED
            )

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"Received data: {data}")

            user = create_user_service(data)
            user_data = {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'phone': user.phone,
                'gender': user.gender,
                'image': user.image,
                'status': user.status,
                'role': 'admin' if user.groups.filter(name='admin').exists() or user.is_superuser else 'user'
            }

            return success_response("Create user success", user_data)
        except ValueError as e:
            return error_response(f"Validation error: {str(e)}")
        except Exception as e:
            print(f"Error in create_user view: {str(e)}")
            return error_response(f"Failed to create user: {str(e)}")
    return error_response("Method not allowed", status_code=405)

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    if request.method == 'GET':
        try:
            page = request.GET.get("page", "1")
            page_size = request.GET.get("page_size", "10")
            try:
                page = int(page)
                page_size = int(page_size)
            except ValueError:
                return error_response("Invalid page or page_size")

            result = get_users_service(page, page_size)
            # Cập nhật kết quả để thêm role
            for user_data in result.get('data', []):
                user = User.objects.get(id=user_data['id'])
                user_data['role'] = 'admin' if user.groups.filter(name='admin').exists() or user.is_superuser else 'user'

            return success_response("Get list success", result)
        except Exception as e:
            return error_response(str(e))
    return error_response("Method not allowed", status_code=405)

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, user_id):
    if request.method == 'GET':
        try:
            user = get_user_service(user_id)
            if user is None:
                return error_response("User doesn't exist")
            user_data = {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'phone': user.phone,
                'gender': user.gender,
                'image': user.image,
                'status': user.status,
                'role': 'admin' if user.groups.filter(name='admin').exists() or user.is_superuser else 'user'
            }
            return success_response("Get user success", user_data)
        except Exception as e:
            return error_response(str(e))
    return error_response("Method not allowed", status_code=405)

@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            user = update_user_service(user_id, data)
            if user is None:
                return error_response("User doesn't exist")
            user_data = {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'phone': user.phone,
                'gender': user.gender,
                'image': user.image,
                'status': user.status,
                'role': 'admin' if user.groups.filter(name='admin').exists() or user.is_superuser else 'user'
            }
            return success_response("Update user success", user_data)
        except json.JSONDecodeError:
            return error_response("Invalid JSON data")
        except Exception as e:
            return error_response(str(e))
    return error_response("Method not allowed", status_code=405)

@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    if request.method == 'DELETE':
        try:
            user = delete_user_service(user_id)
            if user is None:
                return error_response("User doesn't exist")
            user_data = {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'phone': user.phone,
                'gender': user.gender,
                'image': user.image,
                'status': user.status,
                'role': 'admin' if user.groups.filter(name='admin').exists() or user.is_superuser else 'user'
            }
            return success_response("Delete user success", user_data)
        except Exception as e:
            return error_response(str(e))
    return error_response("Method not allowed", status_code=405)

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    if request.method == 'GET':
        try:
            query = request.GET.get("q", "")
            page = request.GET.get("page", "1")
            page_size = request.GET.get("page_size", "10")
            try:
                page = int(page)
                page_size = int(page_size)
            except ValueError:
                return error_response("Invalid page or page_size")

            result = search_users_service(query, page, page_size)
            # Cập nhật kết quả để thêm role
            for user_data in result.get('data', []):
                user = User.objects.get(id=user_data['id'])
                user_data['role'] = 'admin' if user.groups.filter(name='admin').exists() or user.is_superuser else 'user'

            return success_response("Search users success", result)
        except Exception as e:
            return error_response(str(e))
    return error_response("Method not allowed", status_code=405)