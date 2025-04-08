from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Playlist
from .services import create_playlist, update_playlist, delete_playlist, get_playlist, get_user_playlists
import json

@csrf_exempt
def createPlaylist(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user

        # remove when finishing auth func
        if user.is_anonymous:
            user = authenticate(username='deptrai', password='ratdeptrai')

            if user is not None:
                login(request, user)
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid login credentials for default user'}, status=401)

        playlist, response = create_playlist(data, user)
        return response
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def updatePlaylist(request, id):
    if request.method == 'PUT':
        try:
            playlist = Playlist.objects.get(id=id)
            data = json.loads(request.body)
            user = request.user
            response = update_playlist(playlist, data, user)
            return response
        except Playlist.DoesNotExist:
            return JsonResponse({'message': 'Playlist not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def deletePlaylist(request, id):
    if request.method == 'DELETE':
        try:
            playlist = Playlist.objects.get(id=id)
            user = request.user
            response = delete_playlist(playlist, user)
            return response
        except Playlist.DoesNotExist:
            return JsonResponse({'message': 'Playlist not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

def getPlaylist(request, id):
    if request.method == 'GET':
        try:
            playlist = Playlist.objects.get(id=id)
            user = request.user
            response = get_playlist(playlist, user)
            return response
        except Playlist.DoesNotExist:
            return JsonResponse({'message': 'Playlist not found'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def getPlaylists(request):
    if request.method == 'GET':
        user = request.user

        # remove when finishing auth func
        if user.is_anonymous:
            user = authenticate(username='deptrai', password='ratdeptrai')
            if user is not None:
                login(request, user)
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid login credentials for default user'}, status=401)

        response = getPlaylist(user)
        return response
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def getUserPlaylists(request):
    if request.method == 'GET':
        user = request.user

        # remove when finishing auth func
        if user.is_anonymous:
            user = authenticate(username='deptrai', password='ratdeptrai')
            if user is not None:
                login(request, user)
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid login credentials for default user'}, status=401)

        response = get_user_playlists(user)
        return response
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)