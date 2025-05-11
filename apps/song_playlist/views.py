from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .services import (
    addSongToPlaylist,
    goToArtist,
    view_credits,
    getSongFromPlaylist,
    deleteSongFromPlaylist,
    searchSongFromPlaylist,
)
import json

from ..utils.response import error_response


# Add Song to Playlist
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_song_to_playlist(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            playlist_id = data.get("playlist_id")
            song_id = data.get("song_id")

            if not all([playlist_id, song_id]):
                return error_response("playlist_id and song_id are required", status_code=400)

            user = request.user
            response = addSongToPlaylist(request, playlist_id, song_id, user.id)
            return response
        except json.JSONDecodeError:
            return error_response("Invalid JSON data", status_code=400)
        except Exception as e:
            print(f"Error in add_song_to_playlist: {str(e)}")
            return error_response(f"Internal server error: {str(e)}", status_code=500)
    return error_response("Method not allowed", status_code=405)

# Add to Liked Songs
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_liked_songs_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            song_id = data.get('song_id')
            if not song_id:
                return error_response("song_id is required", status_code=400)

            user = request.user
            response = addSongToPlaylist(request, None, song_id, user.id, is_liked_song=True)
            return response
        except json.JSONDecodeError:
            return error_response("Invalid JSON data", status_code=400)
        except Exception as e:
            print(f"Error in add_to_liked_songs_view: {str(e)}")
            return error_response(f"Internal server error: {str(e)}", status_code=500)
    return error_response("Method not allowed", status_code=405)

# Get Songs from Playlist
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSongsFromPlaylist(request, playlist_id):
    if request.method == 'GET':
        try:
            user = request.user
            response = getSongFromPlaylist(playlist_id, user.id)
            return response
        except Exception as e:
            print(f"Error in getSongsFromPlaylist: {str(e)}")
            return error_response(f"Internal server error: {str(e)}", status_code=500)
    return error_response("Method not allowed", status_code=405)

# Get Liked Songs
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_liked_songs_view(request):
    if request.method == 'GET':
        try:
            user = request.user
            response = getSongFromPlaylist(None, user.id, is_liked_song=True)
            return response
        except Exception as e:
            print(f"Error in get_liked_songs_view: {str(e)}")
            return error_response(f"Internal server error: {str(e)}", status_code=500)
    return error_response("Method not allowed", status_code=405)

# Search Songs from Playlist
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def searchSongsFromPlaylist(request, playlist_id):
    if request.method == 'GET':
        try:
            query = request.GET.get('query', None)
            user = request.user
            response = searchSongFromPlaylist(playlist_id, user.id, query)
            return response
        except Exception as e:
            print(f"Error in searchSongsFromPlaylist: {str(e)}")
            return error_response(f"Internal server error: {str(e)}", status_code=500)
    return error_response("Method not allowed", status_code=405)

# Search Liked Songs
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_liked_songs_view(request):
    if request.method == 'GET':
        try:
            query = request.GET.get('query', None)
            user = request.user
            response = searchSongFromPlaylist(None, user.id, query, is_liked_song=True)
            return response
        except Exception as e:
            print(f"Error in search_liked_songs_view: {str(e)}")
            return error_response(f"Internal server error: {str(e)}", status_code=500)
    return error_response("Method not allowed", status_code=405)

# Delete Song from Playlist
@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteSongFrom_Playlist(request, playlist_id, song_id):
    if request.method == 'DELETE':
        try:
            user = request.user
            response = deleteSongFromPlaylist(playlist_id, song_id, user.id)
            return response
        except Exception as e:
            print(f"Error in deleteSongFrom_Playlist: {str(e)}")
            return error_response(f"Internal server error: {str(e)}", status_code=500)
    return error_response("Method not allowed", status_code=405)

# Remove from Liked Songs
@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_liked_songs_view(request, song_id):
    if request.method == 'DELETE':
        try:
            user = request.user
            response = deleteSongFromPlaylist(None, song_id, user.id, is_liked_song=True)
            return response
        except Exception as e:
            print(f"Error in remove_from_liked_songs_view: {str(e)}")
            return error_response(f"Internal server error: {str(e)}", status_code=500)
    return error_response("Method not allowed", status_code=405)

# Go to Artist
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def go_to_artist(request, artist_id):
    if request.method == 'GET':
        try:
            response = goToArtist(request, artist_id)
            return response
        except Exception as e:
            print(f"Error in go_to_artist: {str(e)}")
            return error_response(f"Internal server error: {str(e)}", status_code=500)
    return error_response("Method not allowed", status_code=405)

# View Credits
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_credits(request, song_id):
    if request.method == 'GET':
        try:
            response = view_credits(request, song_id)
            return response
        except Exception as e:
            print(f"Error in view_credits: {str(e)}")
            return error_response(f"Internal server error: {str(e)}", status_code=500)
    return error_response("Method not allowed", status_code=405)