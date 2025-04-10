from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import (
    addSongToPlaylist, goToArtist, view_credits, getSongFromPlaylist,
    deleteSongFromPlaylist, searchSongFromPlaylist
)
import json

@csrf_exempt
def add_song_to_playlist(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            playlist_id = data.get('playlist_id')
            song_id = data.get('song_id')
            response = addSongToPlaylist(request, playlist_id, song_id)
            return response
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def add_to_liked_songs_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            song_id = data.get('song_id')
            response = addSongToPlaylist(request, None, song_id, is_liked_song=True)
            return response
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def getSongsFromPlaylist(request, playlist_id):
    if request.method == 'GET':
        user_id = request.user.id
        response = getSongFromPlaylist(playlist_id, user_id)
        return response
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def get_liked_songs_view(request):
    if request.method == 'GET':
        user_id = request.user.id
        response = getSongFromPlaylist(None, user_id, is_liked_song=True)
        return response
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def searchSongsFromPlaylist(request, playlist_id):
    if request.method == 'GET':
        user_id = request.user.id
        query = request.GET.get('query', None)
        response = searchSongFromPlaylist(playlist_id, user_id, query)
        return response
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def search_liked_songs_view(request):
    if request.method == 'GET':
        user_id = request.user.id
        query = request.GET.get('query', None)
        response = searchSongFromPlaylist(None, user_id, query, is_liked_song=True)
        return response
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def deleteSongFromPlaylist(request, playlist_id, song_id):
    if request.method == 'DELETE':
        user_id = request.user.id
        response = deleteSongFromPlaylist(playlist_id, song_id, user_id)
        return response
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def remove_from_liked_songs_view(request, song_id):
    if request.method == 'DELETE':
        user_id = request.user.id
        response = deleteSongFromPlaylist(None, song_id, user_id, is_liked_song=True)
        return response
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

def go_to_artist(request, user_id):
    if request.method == 'GET':
        response = goToArtist(request, user_id)
        return response
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

def view_credits(request, song_id):
    if request.method == 'GET':
        response = view_credits(request, song_id)
        return response
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)