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
from django.urls import path
from apps.users.views import create_user, get_user, get_users, update_user, delete_user
from apps.songs.views import create_genre, get_genre, get_genres, update_genre, delete_genre, create_song, get_song, get_songs, update_song, delete_song
from apps.playlists.views import create_playlist, get_playlist, get_playlists, update_playlist, delete_playlist
from apps.chat.views import create_chat, get_chat, get_chats, update_chat, delete_chat

urlpatterns = [
    # Admin page
    path('admin/', admin.site.urls),

    # User management
    path('users/', get_users, name='get_users'),
    path('users/<int:user_id>/', get_user, name='get_user'),
    path('users/create/', create_user, name='create_user'),
    path('users/<int:user_id>/update/', update_user, name='update_user'),
    path('users/<int:user_id>/delete/', delete_user, name='delete_user'),

    # Genre management
    path('genres/', get_genres, name='get_genres'),
    path('genres/<int:genre_id>/', get_genre, name='get_genre'),
    path('genres/create/', create_genre, name='create_genre'),
    path('genres/<int:genre_id>/update/', update_genre, name='update_genre'),
    path('genres/<int:genre_id>/delete/', delete_genre, name='delete_genre'),
    # Song management
    path('songs/', get_songs, name='get_songs'),
    path('songs/<int:song_id>/', get_song, name='get_song'),
    path('songs/create/', create_song, name='create_song'),
    path('songs/<int:song_id>/update/', update_song, name='update_song'),
    path('songs/<int:song_id>/delete/', delete_song, name='delete_song'),

    # Playlist management
    path('playlists/', get_playlists, name='get_playlists'),
    path('playlists/<int:playlist_id>/', get_playlist, name='get_playlist'),
    path('playlists/create/', create_playlist, name='create_playlist'),
    path('playlists/<int:playlist_id>/update/', update_playlist, name='update_playlist'),
    path('playlists/<int:playlist_id>/delete/', delete_playlist, name='delete_playlist'),

    # Chat management
    path('chat/', get_chats, name='get_chats'),
    path('chat/<int:chat_id>/', get_chat, name='get_chat'),
    path('chat/create/', create_chat, name='create_chat'),
    path('chat/<int:chat_id>/update/', update_chat, name='update_chat'),
    path('chat/<int:chat_id>/delete/', delete_chat, name='delete_chat'),
]
