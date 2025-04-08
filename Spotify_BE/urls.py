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
from apps.playlists.views import createPlaylist, updatePlaylist, deletePlaylist, getPlaylist, getUserPlaylists
from apps.song_playlist.views import add_song_to_playlist, go_to_artist, view_credits, getSongsFromPlaylist

urlpatterns = [
    path('admin/', admin.site.urls),

    # User URLs
    path('users/', get_users, name='get_users'),
    path('users/<int:user_id>/', get_user, name='get_user'),
    path('users/create/', create_user, name='create_user'),
    path('users/<int:user_id>/update/', update_user, name='update_user'),
    path('users/<int:user_id>/delete/', delete_user, name='delete_user'),

    # Playlist URLs
    path('playlists/create/', createPlaylist, name='create_playlist'),
    path('playlists/<uuid:id>/update/', updatePlaylist, name='update_playlist'),
    path('playlists/<uuid:id>/delete/', deletePlaylist, name='delete_playlist'),
    path('playlists/<uuid:id>/', getPlaylist, name='get_playlist'),
    path('playlists/', getUserPlaylists, name='get_playlists'),

    # SongPlaylist URLs
    path('song_playlist/create/', add_song_to_playlist, name='create_song_playlist'),
    path('song_playlist/<uuid:id>/delete/', go_to_artist, name='delete_song_playlist'),
    path('song_playlist/<uuid:id>/', view_credits, name='get_song_playlist'),
    path('song_playlist/<uuid:playlist_id>/songs/', getSongsFromPlaylist, name='get_songs_from_playlist'),
]


