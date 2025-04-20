from django.contrib import admin
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
            return format_html('<a href="{}" download>Download Audio</a>', obj.url_audio)
        return "-"

    audio_download_link.short_description = 'Audio Download'

    def video_download_link(self, obj):
        if obj.url_video:
            return format_html('<a href="{}" download>Download Video</a>', obj.url_video)
        return "-"

    video_download_link.short_description = 'Video Download'

    def save_model(self, request, obj, form, change):
        # Set the user to the current admin user if creating a new song
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Pass the current user to the form for new objects
        if not obj:
            form.user = request.user
        return form

class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

admin.site.register(Song, SongAdmin)
admin.site.register(Genre, GenreAdmin)