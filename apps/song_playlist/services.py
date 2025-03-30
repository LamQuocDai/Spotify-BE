from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Song, SongPlaylist, Playlist

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
