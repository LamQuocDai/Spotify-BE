from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Playlist
from apps.users.models import User
from .services import (
    create_playlist,
    update_playlist,
    delete_playlist,
    get_playlist,
    get_user_playlists,
    search_playlists,
    get_all_playlists,
    search_all_playlists,
)
import json

from ..utils.response import error_response


# Create Playlist
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createPlaylist(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user  # Lấy user từ JWTAuthentication
            playlist, response = create_playlist(data, user)
            return response
        except json.JSONDecodeError:
            return error_response("Invalid JSON data", status_code=400)
        except Exception as e:
            print(f"Error in createPlaylist: {str(e)}")
            return error_response(f"Internal server error: {str(e)}", status_code=500)
    return error_response("Method not allowed", status_code=405)

# Update Playlist
@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updatePlaylist(request, id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            user = request.user
            try:
                playlist = Playlist.objects.get(id=id)
            except Playlist.DoesNotExist:
                return error_response("Playlist not found", status_code=404)
            response = update_playlist(playlist, data, user)
            return response
        except json.JSONDecodeError:
            return error_response("Invalid JSON data", status_code=400)
        except Exception as e:
            print(f"Error in updatePlaylist: {str(e)}")
            return error_response(f"Internal server error: {str(e)}", status_code=500)
    return error_response("Method not allowed", status_code=405)

# Delete Playlist
@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deletePlaylist(request, id):
    if request.method == 'DELETE':
        try:
            user = request.user
            try:
                playlist = Playlist.objects.get(id=id)
            except Playlist.DoesNotExist:
                return error_response("Playlist not found", status_code=404)
            response = delete_playlist(playlist, user)
            return response
        except Exception as e:
            print(f"Error in deletePlaylist: {str(e)}")
            return error_response(f"Internal server error: {str(e)}", status_code=500)
    return error_response("Method not allowed", status_code=405)

# Get Playlist
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPlaylist(request, id):
    if request.method == 'GET':
        try:
            user = request.user
            try:
                playlist = Playlist.objects.get(id=id)
            except Playlist.DoesNotExist:
                return error_response("Playlist not found", status_code=404)
            response = get_playlist(playlist, user)
            return response
        except Exception as e:
            print(f"Error in getPlaylist: {str(e)}")
            return error_response(f"Internal server error: {str(e)}", status_code=500)
    return error_response("Method not allowed", status_code=405)

# Get All Playlists
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPlaylists(request):
    if request.method == 'GET':
        try:
            page = request.GET.get("page", "1")
            page_size = request.GET.get("page_size", "10")
            response = get_all_playlists(page, page_size)
            return response
        except Exception as e:
            print(f"Error in getPlaylists: {str(e)}")
            return error_response(f"Internal server error: {str(e)}", status_code=500)
    return error_response("Method not allowed", status_code=405)

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserPlaylists(request, id):
    if request.method == 'GET':
        try:
            user = User.objects.get(id=id)
            response = get_user_playlists(user)
            return response
        except User.DoesNotExist:
            return error_response("User not found", status_code=404)
        except Exception as e:
            print(f"Error in getUserPlaylists: {str(e)}")
            return error_response(f"Internal server error: {str(e)}", status_code=500)
    return error_response("Method not allowed", status_code=405)

# Search Playlists
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def searchPlaylists(request):
    if request.method == 'GET':
        try:
            query = request.GET.get("q", "")
            page = request.GET.get("page", "1")
            page_size = request.GET.get("page_size", "10")
            user = request.user
            response = search_playlists(user, query, page, page_size)
            return response
        except Exception as e:
            print(f"Error in searchPlaylists: {str(e)}")
            return error_response(f"Internal server error: {str(e)}", status_code=500)
    return error_response("Method not allowed", status_code=405)

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def searchAllPlaylists(request):
    if request.method == 'GET':
        try:
            query = request.GET.get("q", "")
            page = request.GET.get("page", "1")
            page_size = request.GET.get("page_size", "10")
            user = request.user
            is_admin = user.groups.filter(name__in=['admin', 'full_role']).exists()
            if not is_admin:
                return error_response("Permission denied", status_code=403)
            response = search_all_playlists(query, page, page_size)
            return response
        except Exception as e:
            print(f"Error in searchAllPlaylists: {str(e)}")
            return error_response(f"Internal server error: {str(e)}", status_code=500)
    return error_response("Method not allowed", status_code=405)