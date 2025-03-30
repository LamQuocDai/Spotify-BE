from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import addSongToPlaylist, goToArtist, view_credits
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
