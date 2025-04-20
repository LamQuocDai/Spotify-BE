from rest_framework import serializers
from .models import Song, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class SongSerializer(serializers.ModelSerializer):
    genre_name = serializers.SerializerMethodField()

    class Meta:
        model = Song
        fields = ['id', 'genre', 'genre_name', 'singer_name', 'song_name',
                 'url_video', 'image', 'url_audio', 'user']
        read_only_fields = ['user']

    def get_genre_name(self, obj):
        return obj.genre.name if obj.genre else None

    def get_audio_download_url(self, obj):
        if obj.url_audio:
            request = self.context.get('request')
            return request.build_absolute_uri(f'/api/songs/{obj.id}/download/audio/')
        return None

    def get_video_download_url(self, obj):
        if obj.url_video:
            request = self.context.get('request')
            return request.build_absolute_uri(f'/api/songs/{obj.id}/download/video/')
        return None