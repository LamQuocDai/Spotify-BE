from django.contrib import admin
from .models import Genre, Song

# Register your models here.
admin.site.register(Genre)
admin.site.register(Song)