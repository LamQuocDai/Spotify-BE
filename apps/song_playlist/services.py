# apps/song_playlist/services.py
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Song, SongPlaylist, Playlist
from ..users.models import User

# -------------------------------HELPER FUNCTIONS------------------------------------
def get_user_or_404(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None

def get_song_or_404(song_id):
    try:
        return Song.objects.get(id=song_id)
    except Song.DoesNotExist:
        return None

def get_playlist_or_create_liked_songs(user, playlist_id=None, is_liked_song=False):
    try:
        if is_liked_song:
            try:
                return Playlist.objects.get(user=user, is_likedSong_playlist=True)
            except Playlist.DoesNotExist:
                return Playlist.objects.create(
                    user=user,
                    title="Liked Songs",
                    is_likedSong_playlist=True
                )
        return Playlist.objects.get(id=playlist_id)
    except Playlist.DoesNotExist:
        return None

def check_playlist_permission(playlist, user):
    if playlist.user != user:
        return False
    return True

# -------------------------------PLAYLIST------------------------------------
def addSongToPlaylist(request, playlist_id, song_id, user_id, is_liked_song=False):
    user = get_user_or_404(user_id)
    if not user:
        return JsonResponse({'message': 'User not found'}, status=404)

    song = get_song_or_404(song_id)
    if not song:
        return JsonResponse({'message': 'Song not found'}, status=404)

    playlist = get_playlist_or_create_liked_songs(user, playlist_id, is_liked_song)
    if not playlist:
        return JsonResponse({'message': 'Playlist not found'}, status=404)

    if not is_liked_song and not check_playlist_permission(playlist, user):
        return JsonResponse({
            'message': 'You do not have permission to modify this playlist'
        }, status=403)

    if SongPlaylist.objects.filter(playlist=playlist, song=song).exists():
        return JsonResponse({'message': f'Song already in {playlist.title}'}, status=400)

    song_playlist = SongPlaylist.objects.create(playlist=playlist, song=song)
    return JsonResponse({
        'message': f'Song {song.song_name} added to {playlist.title}',
        'song_id': str(song_playlist.song.id),
        'playlist_id': str(song_playlist.playlist.id)
    }, status=201)

def getSongFromPlaylist(playlist_id, user_id, is_liked_song=False):
    user = get_user_or_404(user_id)

    playlist = get_playlist_or_create_liked_songs(user, playlist_id, is_liked_song)
    if not playlist:
        return JsonResponse({'message': 'Playlist not found'}, status=404)

    if not is_liked_song and not check_playlist_permission(playlist, user):
        return JsonResponse({
            'message': 'You do not have permission to view this playlist'
        }, status=403)

    song_playlists = playlist.song_playlists.all()
    songs = [
        {
            'id': str(song_playlist.song.id),
            'song_name': song_playlist.song.song_name,
            'singer_name': song_playlist.song.singer_name,
            'genre': song_playlist.song.genre.name if song_playlist.song.genre else None,
            'url_audio': song_playlist.song.url_audio,
            'url_video': song_playlist.song.url_video,
            'image': song_playlist.song.image
        }
        for song_playlist in song_playlists
    ]
    return JsonResponse({
        'message': 'Songs retrieved successfully',
        'songs': songs
    }, status=200)

def deleteSongFromPlaylist(playlist_id, song_id, user_id, is_liked_song=False):
    user = get_user_or_404(user_id)

    if not user:
        return JsonResponse({'message': 'User not found'}, status=404)

    song = get_song_or_404(song_id)
    if not song:
        return JsonResponse({'message': 'Song not found'}, status=404)

    playlist = get_playlist_or_create_liked_songs(user, playlist_id, is_liked_song)
    if not playlist:
        return JsonResponse({'message': 'Playlist not found'}, status=404)

    # if not is_liked_song and not check_playlist_permission(playlist, user):
    #     return JsonResponse({
    #         'message': 'You do not have permission to modify this playlist'
    #     }, status=403)

    try:
        song_playlist = SongPlaylist.objects.get(playlist=playlist, song=song)
        song_playlist.delete()
        return JsonResponse({
            'message': f'Song {song.song_name} removed from {playlist.title}'
        }, status=200)
    except SongPlaylist.DoesNotExist:
        return JsonResponse({'message': f'Song not found in {playlist.title}'}, status=404)

def searchSongFromPlaylist(playlist_id, user_id, query=None, is_liked_song=False):
    user = get_user_or_404(user_id)
    if not user:
        return JsonResponse({'message': 'User not found'}, status=404)

    playlist = get_playlist_or_create_liked_songs(user, playlist_id, is_liked_song)
    if not playlist:
        return JsonResponse({'message': 'Playlist not found'}, status=404)

    if not is_liked_song and not check_playlist_permission(playlist, user):
        return JsonResponse({
            'message': 'You do not have permission to view this playlist'
        }, status=403)

    song_playlists = playlist.song_playlists.all()
    if query:
        song_playlists = song_playlists.filter(
            Q(song__song_name__icontains=query) | Q(song__singer_name__icontains=query)
        )

    songs = [
        {
            'id': str(song_playlist.song.id),
            'song_name': song_playlist.song.song_name,
            'singer_name': song_playlist.song.singer_name,
            'genre': song_playlist.song.genre.name if song_playlist.song.genre else None,
            'url': song_playlist.song.url,
            'image': song_playlist.song.image
        }
        for song_playlist in song_playlists
    ]

    return JsonResponse({
        'message': 'Songs retrieved successfully',
        'songs': songs
    }, status=200)

def goToArtist(request, user_id):
    try:
        artist = User.objects.get(id=user_id)
        return render(request, 'artist-form.html', {'artist': artist})
    except User.DoesNotExist:
        return JsonResponse({'message': 'Artist not found'}, status=404)

def view_credits(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    credits = {
        'song_name': song.song_name,
        'singer_name': song.singer_name,
        'genre': song.genre.name if song.genre else None,
        'url': song.url,
        'image': song.image,
    }
    return render(request, 'credits-detail.html', {'song': song, 'credits': credits})