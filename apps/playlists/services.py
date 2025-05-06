from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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

# -----------------------------HANDLE ---------------------------------
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
    is_admin = user.groups.filter(name__in=['admin', 'full_role']).exists()

    if playlist.user != user and not is_admin:
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
    is_admin = user.groups.filter(name__in=['admin', 'full_role']).exists()

    if playlist.user != user and not is_admin:
        return JsonResponse({
            'message': 'You do not have permission to delete this playlist'
        }, status=403)

    playlist.delete()
    return JsonResponse({
        'message': 'Playlist deleted successfully'
    }, status=200)


def get_playlist(playlist, user):
    is_admin = user.groups.filter(name__in=['admin', 'full_role']).exists()

    if playlist.user != user and not is_admin:
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
            'song_count': playlist.song_playlists.count(),
            'image': playlist.image,
            'is_liked_song': playlist.is_likedSong_playlist,
            'user': get_user_data(playlist.user)
        }
        for playlist in playlists
    ]
    return JsonResponse({
        'message': 'Playlists retrieved successfully',
        'playlists': playlists_data
    }, status=200)

def search_playlists(user, query, page=1, page_size=10):
    playlists = Playlist.objects.filter(user=user).filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    ).order_by('id')

    paginator = Paginator(playlists, page_size)
    try:
        paginated_playlists = paginator.page(page)
    except PageNotAnInteger:
        paginated_playlists = paginator.page(1)
    except EmptyPage:
        paginated_playlists = paginator.page(paginator.num_pages)

    playlists_data = [
        {
            'id': str(playlist.id),
            'title': playlist.title,
            'description': playlist.description,
            'song_count': playlist.song_playlists.count(),
            'image': playlist.image,
            'user': get_user_data(playlist.user)
        }
        for playlist in paginated_playlists
    ]
    print(playlists_data)

    return JsonResponse({
        'message': 'Playlists retrieved successfully',
        'playlists': playlists_data,
        'page': page,
        'page_size': page_size,
        'total_pages': paginator.num_pages,
        'total_playlists': paginator.count
    }, status=200)

def search_all_playlists(query, page=1, page_size=10):
    playlists = Playlist.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    ).order_by('id')

    paginator = Paginator(playlists, page_size)
    try:
        paginated_playlists = paginator.page(page)
    except PageNotAnInteger:
        paginated_playlists = paginator.page(1)
    except EmptyPage:
        paginated_playlists = paginator.page(paginator.num_pages)

    playlists_data = [
        {
            'id': str(playlist.id),
            'title': playlist.title,
            'description': playlist.description,
            'song_count': playlist.song_playlists.count(),
            'image': playlist.image,
            'is_liked_song': playlist.is_likedSong_playlist,
            'user': get_user_data(playlist.user)
        }
        for playlist in paginated_playlists
    ]

    return JsonResponse({
        'message': 'All playlists retrieved successfully',
        'playlists': playlists_data,
        'page': page,
        'page_size': page_size,
        'total_pages': paginator.num_pages,
        'total_playlists': paginator.count
    }, status=200)

def get_all_playlists(page=1, page_size=10):
    playlists = Playlist.objects.all().order_by('id')

    paginator = Paginator(playlists, page_size)
    try:
        paginated_playlists = paginator.page(page)
    except PageNotAnInteger:
        paginated_playlists = paginator.page(1)
    except EmptyPage:
        paginated_playlists = paginator.page(paginator.num_pages)

    playlists_data = [
        {
            'id': str(playlist.id),
            'title': playlist.title,
            'description': playlist.description,
            'song_count': playlist.song_playlists.count(),
            'image': playlist.image,
            'is_liked_song': playlist.is_likedSong_playlist,
            'user': get_user_data(playlist.user)
        }
        for playlist in paginated_playlists
    ]

    return JsonResponse({
        'message': 'All playlists retrieved successfully',
        'playlists': playlists_data,
        'page': page,
        'page_size': page_size,
        'total_pages': paginator.num_pages,
        'total_playlists': paginator.count
    }, status=200)