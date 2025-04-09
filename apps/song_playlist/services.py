from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Song, SongPlaylist, Playlist
from ..users.models import User


def addSongToPlaylist(request, playlist_id, song_id):
    try:
        playlist = Playlist.objects.get(id=playlist_id)
        song = Song.objects.get(id=song_id)
    except Playlist.DoesNotExist:
        return JsonResponse({'message': 'Playlist not found'}, status=404)
    except Song.DoesNotExist:
        return JsonResponse({'message': 'Song not found'}, status=404)

    song_playlist = SongPlaylist.objects.create(playlist=playlist, song=song)
    return JsonResponse({
        'message': f'Song {song.song_name} added to {playlist.title}',
        'song_id': song_playlist.song.id,
        'playlist_id': song_playlist.playlist.id
    }, status=201)

def getSongFromPlaylist(playlist_id, user_id):
    try:
        playlist = Playlist.objects.get(id=playlist_id)
        user = User.objects.get(id=user_id)

        if playlist.user != user:
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
                'url': song_playlist.song.url,
                'image': song_playlist.song.image
            }
            for song_playlist in song_playlists
        ]
        return JsonResponse({
            'message': 'Songs retrieved successfully',
            'songs': songs
        }, status=200)
    except Playlist.DoesNotExist:
        return JsonResponse({'message': 'playlist not found'}, status=404)
    except User.DoesNotExist:
        return JsonResponse({'message': 'user not found'}, status=404)

def goToArtist(request, user_id):
    try:
        artist = Song.user.objects.get(id=user_id)
        return render(request, 'artist-form.html', {'artist': artist})
    except Song.user.DoesNotExist:
        return JsonResponse({'message': 'Artist not found'}, status=404)

def view_credits(request, song_id):
    song = get_object_or_404(Song, id=song_id)

    credits = {
        'song_name': song.song_name,
        'singer_name': song.singer_name,
        'genre': song.genre.name,
        'url': song.url,
        'image': song.image,
    }

    return render(request, 'credits-detail.html', {'song': song, 'credits': credits})

def deleteSongFromPlaylist(playlist_id, song_id, user_id):
    try:
        playlist = Playlist.objects.get(id=playlist_id)
        song = Song.objects.get(id=song_id)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)

        if playlist.user != user:
            return JsonResponse({
                'message': 'You do not have permission to modify this playlist'
            }, status=403)

        song_playlist = SongPlaylist.objects.get(playlist=playlist, song=song)
        song_playlist.delete()
        return JsonResponse({
            'message': f'Song {song.song_name} removed from {playlist.title}'
        }, status=200)

    except Playlist.DoesNotExist:
        return JsonResponse({'message': 'Playlist not found'}, status=404)
    except Song.DoesNotExist:
        return JsonResponse({'message': 'Song not found'}, status=404)
    except SongPlaylist.DoesNotExist:
        return JsonResponse({'message': 'Song not found in this playlist'}, status=404)

def searchSongFromPlaylist(playlist_id, user_id, query=None):
    try:
        playlist = Playlist.objects.get(id=playlist_id)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)

        if playlist.user != user:
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

    except Playlist.DoesNotExist:
        return JsonResponse({'message': 'Playlist not found'}, status=404)


