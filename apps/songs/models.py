from django.db import models
from apps.users.models import User
import uuid

class Genre(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Song(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='songs')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_songs')
    singer_name = models.CharField(max_length=100)
    song_name = models.CharField(max_length=100)
    url = models.URLField(max_length=1000)
    image = models.URLField(max_length=10000, blank=True, null=True)

    def __str__(self):
        return self.singer_name
