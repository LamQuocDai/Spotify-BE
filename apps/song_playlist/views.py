from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from .services import addSongToPlaylist, goToArtist, view_credits, getSongFromPlaylist
from .models import Song
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

def go_to_artist(request, user_id):
    if request.method == 'GET':
        try:
            response = goToArtist(request, user_id)
            return response
        except Song.user.DoesNotExist:
            return JsonResponse({'message': 'Artist not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

def view_credits(request, song_id):
    if request.method == 'GET':
        try:
            response = view_credits(request, song_id)
            return response
        except Song.DoesNotExist:
            return JsonResponse({'message': 'Song not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def getSongsFromPlaylist(request, playlist_id):
    if request.method == 'GET':
        user_id = request.user.id

        if user_id is None:
            user = authenticate(username='deptrai', password='ratdeptrai')
            if user is not None:
                login(request, user)
                user_id = user.id
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid login credentials for default user'},
                                    status=401)

        response = getSongFromPlaylist(playlist_id, user_id)
        return response
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
