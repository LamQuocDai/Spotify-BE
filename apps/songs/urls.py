from django.urls import path
from . import views

urlpatterns = [
    # Genre management
    path('genres/', views.get_genres, name='get_genres'),
    path('genres/<int:genre_id>/', views.get_genre, name='get_genre'),
    path('genres/create/', views.create_genre, name='create_genre'),
    path('genres/<int:genre_id>/update/', views.update_genre, name='update_genre'),
    path('genres/<int:genre_id>/delete/', views.delete_genre, name='delete_genre'),
    # Song management
    path('', views.get_songs, name='get_songs'),
    path('<int:song_id>/', views.get_song, name='get_song'),
    path('create/', views.create_song, name='create_song'),
    path('<int:song_id>/update/', views.update_song, name='update_song'),
    path('<int:song_id>/delete/', views.delete_song, name='delete_song'),
]