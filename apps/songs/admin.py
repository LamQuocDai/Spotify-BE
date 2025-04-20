from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Song, Genre
from .form import SongForm

class SongAdmin(admin.ModelAdmin):
    form = SongForm
    list_display = ['song_name', 'singer_name', 'genre', 'user', 'audio_download_link', 'video_download_link']
    list_filter = ['genre', 'user']
    search_fields = ['song_name', 'singer_name']

    def audio_download_link(self, obj):
        if obj.url_audio:
            url = reverse('song-download', kwargs={'pk': obj.pk, 'file_type': 'audio'})
            return format_html('<a href="{}" download>Download Audio</a>', url)
        return "-"

    audio_download_link.short_description = 'Audio Download'

    def video_download_link(self, obj):
        if obj.url_video:
            url = reverse('song-download', kwargs={'pk': obj.pk, 'file_type': 'video'})
            return format_html('<a href="{}" download>Download Video</a>', url)
        return "-"

    video_download_link.short_description = 'Video Download'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            form.user = request.user
        return form

class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

admin.site.register(Song, SongAdmin)
admin.site.register(Genre, GenreAdmin)