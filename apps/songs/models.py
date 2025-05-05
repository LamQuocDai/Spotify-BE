from django.db import models
from apps.users.models import User
import uuid

class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Song(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='songs')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_songs')
    singer_name = models.CharField(max_length=100)
    song_name = models.CharField(max_length=100) 
    url_video = models.URLField(max_length=1000, blank=True, null=True)
    image = models.URLField(max_length=1000, blank=True, null=True)
    url_audio = models.URLField(max_length=1000)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.singer_name} - {self.song_name}"

    class Meta:
        indexes = [
            models.Index(fields=['song_name']),
            models.Index(fields=['genre']),
            models.Index(fields=['-create_at']),
        ]