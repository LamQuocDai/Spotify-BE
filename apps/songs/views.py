import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.http import StreamingHttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Song, Genre
from .serializers import SongSerializer, GenreSerializer
from .form import SongForm
from .aws_helper import S3Uploader
import logging
import urllib.parse

logger = logging.getLogger(__name__)

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class SongViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Song.objects.all()

    def list(self, request):
        genre_id = request.query_params.get('genre', None)
        user_id = request.query_params.get('user', None)

        queryset = self.get_queryset()

        if genre_id:
            queryset = queryset.filter(genre_id=genre_id)

        if user_id:
            queryset = queryset.filter(user_id=user_id)

        serializer = SongSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        song = get_object_or_404(Song, pk=pk)
        serializer = SongSerializer(song)
        return Response(serializer.data)

    def create(self, request):
        form = SongForm(data=request.data, files=request.FILES)
        if form.is_valid():
            song = form.save(user=request.user)
            serializer = SongSerializer(song)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        song = get_object_or_404(Song, pk=pk)

        if song.user != request.user:
            return Response({'error': 'You do not have permission to update this song'},
                            status=status.HTTP_403_FORBIDDEN)

        # Initialize form with existing instance and new data
        form = SongForm(data=request.data, files=request.FILES, instance=song)
        if form.is_valid():
            song = form.save()
            serializer = SongSerializer(song)
            return Response(serializer.data)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        song = get_object_or_404(Song, pk=pk)

        if song.user != request.user:
            return Response({'error': 'You do not have permission to delete this song'},
                            status=status.HTTP_403_FORBIDDEN)

        s3_uploader = S3Uploader()
        if song.url_audio:
            s3_uploader.delete_file(song.url_audio)
        if song.image:
            s3_uploader.delete_file(song.image)
        if song.url_video:
            s3_uploader.delete_file(song.url_video)

        song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], url_path='download/(?P<file_type>audio|video)')
    def download(self, request, pk=None, file_type=None):
        song = get_object_or_404(Song, pk=pk)

        # Determine which file to download
        if file_type == 'audio':
            file_url = song.url_audio
            content_type = 'audio/mpeg'  # Adjust based on file type
            file_extension = file_url.split('.')[-1] if file_url else 'mp3'
            file_name = f"{song.singer_name}_{song.song_name}_audio.{file_extension}"
        elif file_type == 'video':
            file_url = song.url_video
            if not file_url:
                return Response({'error': 'No video file available for this song'},
                                status=status.HTTP_404_NOT_FOUND)
            content_type = 'video/mp4'  # Adjust based on file type
            file_extension = file_url.split('.')[-1] if file_url else 'mp4'
            file_name = f"{song.singer_name}_{song.song_name}_video.{file_extension}"
        else:
            return Response({'error': 'Invalid file type'}, status=status.HTTP_400_BAD_REQUEST)

        if not file_url:
            return Response({'error': f'No {file_type} file available for this song'},
                            status=status.HTTP_404_NOT_FOUND)

        # Stream the file from S3
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )
            key = file_url.split('.com/')[-1]
            response = s3_client.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
            file_stream = response['Body']

            # Create streaming response
            encoded_file_name = urllib.parse.quote(file_name)
            streaming_response = StreamingHttpResponse(
                file_stream,
                content_type=content_type
            )
            streaming_response['Content-Disposition'] = f'attachment; filename="{encoded_file_name}"'
            streaming_response['Content-Length'] = response['ContentLength']
            return streaming_response

        except ClientError as e:
            logger.error(f"Error downloading from S3: {e}")
            return Response({'error': f'Failed to download {file_type} file'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)