import requests
import uuid
from django.db import transaction
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from social_django.models import UserSocialAuth
import logging
from django.core.cache import cache

from Spotify_BE import settings
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer, SocialLoginSerializer
from .models import User

# Set up logging
logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

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

class SocialLoginView(generics.GenericAPIView):
    serializer_class = SocialLoginSerializer
    permission_classes = [permissions.AllowAny]

    # Google OAuth URLs
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    def post(self, request, *args, **kwargs):
        # Validate request data
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error("Serializer errors: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        code = serializer.validated_data['code']
        logger.info("Processing Google login: code=%s", code[:10] + "...")

        # Check for code reuse
        cache_key = f"auth_code:{code}"
        if cache.get(cache_key):
            logger.warning("Authorization code already used: %s", code[:10] + "...")
            return Response(
                {'detail': 'Authorization code has already been used'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Get access token
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

            # Cache the code
            cache.set(cache_key, True, timeout=60)

            # Get user info
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

            # Create or update user
            with transaction.atomic():
                user, created = User.objects.select_for_update().get_or_create(
                    email=email,
                    defaults={
                        'username': email.split('@')[0][:15],  # Base username
                        'first_name': name.split()[0] if name and ' ' in name else name,
                        'last_name': ' '.join(name.split()[1:]) if name and ' ' in name else '',
                        'image': picture,
                    }
                )
                if created:
                    user.set_unusable_password()
                    user.save()
                    logger.info("Created new user: username=%s, email=%s", user.username, email)
                else:
                    # Update existing user
                    user.first_name = name.split()[0] if name and ' ' in name else name
                    user.last_name = ' '.join(name.split()[1:]) if name and ' ' in name else ''
                    user.image = picture
                    user.save()
                    logger.info("Updated user: username=%s, email=%s", user.username, email)

                # Handle username collisions
                if created and User.objects.filter(username=user.username).exclude(id=user.id).exists():
                    user.username = f"{user.username[:10]}_{uuid.uuid4().hex[:4]}"
                    user.save()
                    logger.info("Updated username due to collision: %s", user.username)

                # Create or update social auth
                social_auth, social_created = UserSocialAuth.objects.update_or_create(
                    user=user,
                    provider='google',
                    defaults={'uid': provider_id}
                )
                logger.info("Social auth %s: user=%s, uid=%s",
                           "created" if social_created else "updated", user.username, provider_id)

                # Generate tokens
                refresh = RefreshToken.for_user(user)
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