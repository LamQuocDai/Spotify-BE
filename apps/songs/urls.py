from django.urls import path
from .views import create_genre, get_genre, get_genres, update_genre, delete_genre, create_song, get_song, get_songs, update_song, delete_song

urlpatterns = [
    # Genre management
    path('genres/', get_genres, name='get_genres'),
    path('genres/<int:genre_id>/', get_genre, name='get_genre'),
    path('genres/create/', create_genre, name='create_genre'),
    path('genres/<int:genre_id>/update/', update_genre, name='update_genre'),
    path('genres/<int:genre_id>/delete/', delete_genre, name='delete_genre'),
    # Song management
    path('', get_songs, name='get_songs'),
    path('<int:song_id>/', get_song, name='get_song'),
    path('create/', create_song, name='create_song'),
    path('<int:song_id>/update/', update_song, name='update_song'),
    path('<int:song_id>/delete/', delete_song, name='delete_song'),
]