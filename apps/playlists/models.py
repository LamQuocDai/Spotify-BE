from django.db import models
from apps.users.models import User
from apps.songs.models import Song

class Playlist(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SongPlaylist(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='playlist_songs')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='song_playlists')

class PlaylistUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_playlists')
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='playlist_users')
