from django import forms
from .models import Song
from .aws_helper import S3Uploader
import logging

logger = logging.getLogger(__name__)

class SongForm(forms.ModelForm):
    audio_file = forms.FileField(required=False, label='Audio File')
    image_file = forms.ImageField(required=False, label='Image File')
    video_file = forms.FileField(required=False, label='Video File')

    class Meta:
        model = Song
        fields = ['genre', 'singer_name', 'song_name', 'audio_file', 'image_file', 'video_file']

    def clean_audio_file(self):
        audio_file = self.cleaned_data.get('audio_file')
        if audio_file:
            name = audio_file.name.lower()
            if not (name.endswith('.mp3') or name.endswith('.mp4') or name.endswith('.wav')):
                raise forms.ValidationError("Only MP3, MP4, or WAV audio files are allowed.")
            if audio_file.size > 100 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 100MB.")
        return audio_file

    def clean_video_file(self):
        video_file = self.cleaned_data.get('video_file')
        if video_file:
            name = video_file.name.lower()
            if not (name.endswith('.mp4') or name.endswith('.mov') or name.endswith('.avi')):
                raise forms.ValidationError("Only MP4, MOV, or AVI video files are allowed.")
            if video_file.size > 200 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 200MB.")
        return video_file

    def clean_image_file(self):
        image_file = self.cleaned_data.get('image_file')
        if image_file:
            name = image_file.name.lower()
            if not (name.endswith('.jpg') or name.endswith('.jpeg') or name.endswith('.png')):
                raise forms.ValidationError("Only JPG, JPEG, or PNG image files are allowed.")
            if image_file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 10MB.")
        return image_file

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        s3_uploader = S3Uploader()

        # Delete old files if they exist and new files are uploaded
        if self.instance.pk:
            try:
                old_song = Song.objects.get(pk=self.instance.pk)
                if self.cleaned_data.get('audio_file') and old_song.url_audio:
                    s3_uploader.delete_file(old_song.url_audio)
                if self.cleaned_data.get('image_file') and old_song.image:
                    s3_uploader.delete_file(old_song.image)
                if self.cleaned_data.get('video_file') and old_song.url_video:
                    s3_uploader.delete_file(old_song.url_video)
            except Song.DoesNotExist:
                pass

        # Handle audio file
        audio_file = self.cleaned_data.get('audio_file')
        if audio_file:
            url_audio = s3_uploader.upload_file(audio_file, 'song')
            if url_audio:
                instance.url_audio = url_audio
            else:
                logger.error("Failed to upload audio file to S3")
                raise forms.ValidationError("Failed to upload audio file.")
        elif 'url_audio' in self.data:  # giữ giá trị cũ khi không thay đổi file
            instance.url_audio = self.data['url_audio']
        elif not instance.url_audio:
            raise forms.ValidationError("Audio file or URL is required.")

        # Handle image file
        image_file = self.cleaned_data.get('image_file')
        if image_file:
            image_url = s3_uploader.upload_file(image_file, 'image')
            if image_url:
                instance.image = image_url
            else:
                logger.error("Failed to upload image file to S3")
                raise forms.ValidationError("Failed to upload image file.")
        elif 'image' in self.data:
            instance.image = self.data['image']

        # Handle video file
        video_file = self.cleaned_data.get('video_file')
        if video_file:
            url_video = s3_uploader.upload_file(video_file, 'video')
            if url_video:
                instance.url_video = url_video
            else:
                logger.error("Failed to upload video file to S3")
                raise forms.ValidationError("Failed to upload video file.")
        elif 'url_video' in self.data:
            instance.url_video = self.data['url_video']

        # Set user if provided (for admin, user might be passed)
        if user:
            instance.user = user

        if commit:
            instance.save()
        return instance