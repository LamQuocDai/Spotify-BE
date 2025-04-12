from django.urls import path
from .views import create_playlist, get_playlist, get_playlists, update_playlist, delete_playlist

urlpatterns = [
    path('', get_playlists, name='get_playlists'),
    path('<int:playlist_id>/', get_playlist, name='get_playlist'),
    path('create/', create_playlist, name='create_playlist'),
    path('<int:playlist_id>/update/', update_playlist, name='update_playlist'),
    path('<int:playlist_id>/delete/', delete_playlist, name='delete_playlist'),
]