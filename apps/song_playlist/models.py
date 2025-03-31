from django.db import models
from apps.songs.models import Song
from apps.playlists.models import Playlist
import uuid

class SongPlaylist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='song_playlists')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='song_playlists')

    def __str__(self):
        return f"{self.song.song_name} in {self.playlist.title}"
