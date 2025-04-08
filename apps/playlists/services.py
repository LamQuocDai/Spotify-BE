from .models import Playlist

def create_playlist_service(data):
    try:
        playlist = Playlist.objects.create(
            title=data['title'],
            description=data['description'],
        )
        return playlist
    except Exception as e:
        return None

def get_playlists_service():
    return list(Playlist.objects.all().values())

def get_playlist_service(playlist_id):
    try:
        playlist = Playlist.objects.get(id=playlist_id)
        return playlist
    except Playlist.DoesNotExist:
        return None
    except Playlist.MultipleObjectsReturned:
        return None

def update_playlist_service(playlist_id, data):
    try:
        playlist = Playlist.objects.get(id=playlist_id)
        playlist.title = data.get('title', playlist.title)
        playlist.description = data.get('description', playlist.description)

        playlist.save()
        return playlist
    except Playlist.DoesNotExist:
        return None
    except Playlist.MultipleObjectsReturned:
        return None

def delete_playlist_service(playlist_id):
    try:
        playlist = Playlist.objects.get(id=playlist_id)
        playlist.delete()
        return playlist
    except Playlist.DoesNotExist:
        return None
    except Playlist.MultipleObjectsReturned:
        return None
