from django.contrib import admin
from .models import SongPlaylist, Song, Playlist

# Register your models here.
admin.site.register(Song)
admin.site.register(SongPlaylist)
admin.site.register(Playlist)
