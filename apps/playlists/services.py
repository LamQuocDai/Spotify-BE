from django.http import JsonResponse
from .models import Playlist


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
        user=user
    )
    return playlist, JsonResponse({
        'message': 'Playlist created successfully',
        'id': str(playlist.id),
        'title': playlist.title,
        'description': playlist.description
    }, status=201)


def update_playlist(playlist, data, user):
    if playlist.user != user:
        return JsonResponse({
            'message': 'You do not have permission to edit this playlist'
        }, status=403)

    playlist.title = data.get('title', playlist.title)
    playlist.description = data.get('description', playlist.description)
    playlist.save()
    return JsonResponse({
        'message': 'Playlist updated successfully',
        'id': str(playlist.id),
        'title': playlist.title,
        'description': playlist.description
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
        'description': playlist.description
    }, status=200)

def get_user_playlists(user):
    if not user.is_authenticated:
        return JsonResponse({
            'message': 'User not authenticated'
        }, status=401)

    playlists = Playlist.objects.filter(user=user)
    playlists_data = [
        {
            'id': str(playlist.id),
            'title': playlist.title,
            'description': playlist.description,
            'song_count': playlist.song_playlists.count()
        }
        for playlist in playlists
    ]
    return JsonResponse({
        'message': 'Playlists retrieved successfully',
        'playlists': playlists_data
    }, status=200)