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
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
# from apps.users.views import CustomTokenObtainPairView
from django.urls import path
from apps.users.views import create_user, get_user, get_users, update_user, delete_user
from apps.playlists.views import createPlaylist, updatePlaylist, deletePlaylist, getPlaylist, getPlaylists, searchPlaylists
from apps.users.views import create_user, get_user, get_users, update_user, delete_user
from apps.playlists.views import createPlaylist, updatePlaylist, deletePlaylist, getPlaylist, getPlaylists, searchPlaylists, getUserPlaylists, searchAllPlaylists
from apps.song_playlist.views import (
    add_song_to_playlist, go_to_artist, view_credits, getSongsFromPlaylist,
    deleteSongFrom_Playlist, searchSongsFromPlaylist, add_to_liked_songs_view,
    get_liked_songs_view, remove_from_liked_songs_view, search_liked_songs_view,
 )

urlpatterns = [
    path('admin/', admin.site.urls),

    # User management
    path('users/', include('apps.users.urls')),
    # Song management
    path('api/', include('apps.songs.urls')),

    # # Chat management
    path('api/', include('apps.chat.urls')),

    # path('api/jwt/token/', CustomTokenObtainPairView.as_view(permission_classes=[AllowAny]), name='token_obtain_pair'),
    path('api/jwt/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/jwt/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/', ObtainAuthToken.as_view(), name='api_token_auth'),

    # User URLs
    path('users/', get_users, name='get_users'),
    path('users/<uuid:user_id>/', get_user, name='get_user'),
    path('users/create/', create_user, name='create_user'),
    path('users/<uuid:user_id>/update/', update_user, name='update_user'),
    path('users/<uuid:user_id>/delete/', delete_user, name='delete_user'),

    #Playlist URLs
    path('playlists/', getPlaylists, name='get_playlists'),
    path('playlists/create/', createPlaylist, name='create_playlist'),
    path('playlists/<uuid:id>/update/', updatePlaylist, name='update_playlist'),
    path('playlists/<uuid:id>/delete/', deletePlaylist, name='delete_playlist'),
    path('playlists/<uuid:id>/', getPlaylist, name='get_playlist'),
    path('playlists/<uuid:id>/user', getUserPlaylists, name='get_user_playlist'),
    path('playlists/search/', searchPlaylists, name='search_playlists'),
    path('playlists/search-all/', searchAllPlaylists, name='search_all_playlists'),  # New endpoint

    # SongPlaylist URLs
    path('song_playlist/create/', add_song_to_playlist, name='create_song_playlist'),
    path('song_playlist/<uuid:playlist_id>/songs/', getSongsFromPlaylist, name='get_songs_from_playlist'),
    path('song_playlist/<uuid:playlist_id>/songs/search/', searchSongsFromPlaylist, name='search_songs_from_playlist'),
    path('song_playlist/<uuid:playlist_id>/songs/<uuid:song_id>/delete/', deleteSongFrom_Playlist, name='delete_song_from_playlist'),
    path('song_playlist/<uuid:id>/delete/', go_to_artist, name='delete_song_playlist'),
    path('song_playlist/<uuid:id>/', view_credits, name='get_song_playlist'),
    path('song_playlist/liked_songs/add/', add_to_liked_songs_view, name='add_to_liked_songs'),
    path('song_playlist/liked_songs/', get_liked_songs_view, name='get_liked_songs'),
    path('song_playlist/liked_songs/search/', search_liked_songs_view, name='search_liked_songs'),
    path('song_playlist/liked_songs/<uuid:song_id>/remove/', remove_from_liked_songs_view, name='remove_from_liked_songs'),
]
