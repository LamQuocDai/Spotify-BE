# Spotify_BE/urls.py
from django.contrib import admin
from django.urls import path
from apps.users.views import create_user, get_user, get_users, update_user, delete_user
from apps.playlists.views import createPlaylist, updatePlaylist, deletePlaylist, getPlaylist, getPlaylists, searchPlaylists
from apps.song_playlist.views import (
    add_song_to_playlist, go_to_artist, view_credits, getSongsFromPlaylist,
    deleteSongFromPlaylist, searchSongsFromPlaylist, add_to_liked_songs_view,
    get_liked_songs_view, remove_from_liked_songs_view, search_liked_songs_view
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # User URLs
    path('users/', get_users, name='get_users'),
    path('users/<int:user_id>/', get_user, name='get_user'),
    path('users/create/', create_user, name='create_user'),
    path('users/<int:user_id>/update/', update_user, name='update_user'),
    path('users/<int:user_id>/delete/', delete_user, name='delete_user'),

    # Playlist URLs
    path('playlists/', getPlaylists, name='get_playlists'),
    path('playlists/create/', createPlaylist, name='create_playlist'),
    path('playlists/<uuid:id>/update/', updatePlaylist, name='update_playlist'),
    path('playlists/<uuid:id>/delete/', deletePlaylist, name='delete_playlist'),
    path('playlists/<uuid:id>/', getPlaylist, name='get_playlist'),
    path('playlists/search/', searchPlaylists, name='search_playlists'),

    # SongPlaylist URLs
    path('song_playlist/create/', add_song_to_playlist, name='create_song_playlist'),
    path('song_playlist/<uuid:playlist_id>/songs/', getSongsFromPlaylist, name='get_songs_from_playlist'),
    path('song_playlist/<uuid:playlist_id>/songs/search/', searchSongsFromPlaylist, name='search_songs_from_playlist'),
    path('song_playlist/<uuid:playlist_id>/songs/<uuid:song_id>/delete/', deleteSongFromPlaylist, name='delete_song_from_playlist'),
    path('song_playlist/<uuid:id>/delete/', go_to_artist, name='delete_song_playlist'),
    path('song_playlist/<uuid:id>/', view_credits, name='get_song_playlist'),
    path('song_playlist/liked_songs/add/', add_to_liked_songs_view, name='add_to_liked_songs'),
    path('song_playlist/liked_songs/', get_liked_songs_view, name='get_liked_songs'),
    path('song_playlist/liked_songs/search/', search_liked_songs_view, name='search_liked_songs'),
    path('song_playlist/liked_songs/<uuid:song_id>/remove/', remove_from_liked_songs_view, name='remove_from_liked_songs'),
]