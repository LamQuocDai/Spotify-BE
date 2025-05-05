from django.db import models
from apps.users.models import User
from apps.songs.models import Song
import uuid

class Playlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    create_date = models.DateTimeField(auto_now_add=True)
    image = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_playlist', null=False)
    is_likedSong_playlist = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                condition=models.Q(is_likedSong_playlist=True),
                name='unique_liked_song_playlist_per_user'
            )
        ]

        permissions = [
            ("search_playlist", "Can search playlists"),
        ]

