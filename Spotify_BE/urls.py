"""
URL configuration for Spotify_BE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    # Admin page
    path('admin/', admin.site.urls),

    # User management
    path('users/', include('apps.users.urls')),

    # Song management
    path('api/', include('apps.songs.urls')),

    # Playlist management
    path('playlists/', include('apps.playlists.urls')),

    # # Chat management
    path('chat/', include('apps.chat.urls')),

    path('api/jwt/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/jwt/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/jwt/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/', ObtainAuthToken.as_view(), name='api_token_auth'),
]
