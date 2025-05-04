# services.py
from django.db.models import Q
from django.http import JsonResponse
from .models import Playlist
import re

# ------------------------ HELPER FUNCTION --------------------------
def validate_base64_image(base64_string):
    if not base64_string:
        return True
    pattern = r'^data:image/(png|jpeg|jpg);base64,'
    return bool(re.match(pattern, base64_string))

def get_user_data(user):
    return {
        'id': str(user.id),
        'username': user.username,
        'email': user.email,
        'phone': user.phone,
        'gender': user.gender,
        'image': user.image,
        'status': user.status,
    }

# ------------------------ SERVICE --------------------------
def create_playlist(data, user):
    title = data.get('title')
    description = data.get('description')

    if not title or not description:
        return None, JsonResponse({
            'status': 'error', 'message': 'Title and description are required'
        }, status=400)

    playlist = Playlist.objects.create(
        title=title,
        description=description,
        image=None,
        user=user
    )
    return playlist, JsonResponse({
        'message': 'Playlist created successfully',
        'id': str(playlist.id),
        'title': playlist.title,
        'description': playlist.description,
        'image': playlist.image,
        'user': get_user_data(playlist.user)
    }, status=201)

def update_playlist(playlist, data, user):
    if playlist.user != user:
        return JsonResponse({
            'message': 'You do not have permission to edit this playlist'
        }, status=403)

    title = data.get('title', playlist.title)
    description = data.get('description', playlist.description)
    image = data.get('image', playlist.image)

    if image and not validate_base64_image(image):
        return JsonResponse({
            'status': 'error', 'message': 'Invalid base64 image format'
        }, status=400)

    playlist.title = title
    playlist.description = description
    playlist.image = image
    playlist.save()
    return JsonResponse({
        'message': 'Playlist updated successfully',
        'id': str(playlist.id),
        'title': playlist.title,
        'description': playlist.description,
        'image': playlist.image,
        'user': get_user_data(playlist.user)
    }, status=200)

def delete_playlist(playlist, user):
    if playlist.user != user:
        return JsonResponse({
            'message': 'You do not have permission to delete this playlist'
        }, status=403)

    playlist.delete()
    return JsonResponse({
        'message': 'Playlist deleted successfully'
    }, status=200)

def get_playlist(playlist, user):
    if playlist.user != user:
        return JsonResponse({
            'message': 'You do not have permission to view this playlist'
        }, status=403)

    return JsonResponse({
        'id': str(playlist.id),
        'title': playlist.title,
        'description': playlist.description,
        'image': playlist.image,
        'is_liked_song': playlist.is_likedSong_playlist,
        'user': get_user_data(playlist.user)
    }, status=200)

def get_user_playlists(user, page=1, size=10):
    if not user.is_authenticated:
        return JsonResponse({
            'message': 'User not authenticated'
        }, status=401)

    playlists = Playlist.objects.filter(user=user)
    total = playlists.count()
    playlists = playlists[(page - 1) * size:page * size]
    playlists_data = [
        {
            'id': str(playlist.id),
            'title': playlist.title,
            'description': playlist.description,
            'image': playlist.image,
            'song_count': playlist.song_playlists.count(),
            'is_liked_song': playlist.is_likedSong_playlist,
            'user': get_user_data(playlist.user)
        }
        for playlist in playlists
    ]
    return JsonResponse({
        'message': 'Playlists retrieved successfully',
        'playlists': playlists_data,
        'count': total
    }, status=200)

def search_playlists(user, query, page=1, size=10):
    if not user.is_authenticated:
        return JsonResponse({
            'message': 'User not authenticated'
        }, status=401)

    playlists = Playlist.objects.filter(user=user).filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )
    total = playlists.count()
    playlists = playlists[(page - 1) * size:page * size]
    playlists_data = [
        {
            'id': str(playlist.id),
            'title': playlist.title,
            'description': playlist.description,
            'image': playlist.image,
            'song_count': playlist.song_playlists.count(),
            'user': get_user_data(playlist.user)
        }
        for playlist in playlists
    ]
    return JsonResponse({
        'message': 'Playlists retrieved successfully',
        'playlists': playlists_data,
        'count': total
    }, status=200)