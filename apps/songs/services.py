from .models import Song, Genre

def create_genre_service(data):
    try:
        genre = Genre.objects.create(
            name=data['name'],
        )
        return genre
    except Exception as e:
        return None

def get_genres_service():
    return list(Genre.objects.all().values())

def get_genre_service(genre_id):
    try:
        genre = Genre.objects.get(id=genre_id)
        return genre
    except Genre.DoesNotExist:
        return None
    except Genre.MultipleObjectsReturned:
        return None

def update_genre_service(genre_id, data):
    try:
        genre = Genre.objects.get(id=genre_id)
        genre.name = data.get('name', genre.name)

        genre.save()
        return genre
    except Genre.DoesNotExist:
        return None
    except Genre.MultipleObjectsReturned:
        return None

def delete_genre_service(genre_id):
    try:
        genre = Genre.objects.get(id=genre_id)
        genre.delete()
        return genre
    except Genre.DoesNotExist:
        return None
    except Genre.MultipleObjectsReturned:
        return None


def create_song_service(data):
    try:
        song = Song.objects.create(
            genre_id=data['genre_id'],
            user_id=data['user_id'],
            singer_name=data['singer_name'],
            song_name=data['song_name'],
            url_video=data['url_video'],
            url_audio=data['url_audio'],
            image=data['image'],
        )
        return song
    except Exception as e:
        return None

def get_songs_service():
    return list(Song.objects.all().values())

def get_song_service(song_id):
    try:
        song = Song.objects.get(id=song_id)
        return song
    except Song.DoesNotExist:
        return None
    except Song.MultipleObjectsReturned:
        return None

def update_song_service(song_id, data):
    try:
        song = Song.objects.get(id=song_id)
        song.genre_id = data.get('genre_id', song.genre_id)
        song.song_name = data.get('song_name', song.song_name)
        song.singer_name = data.get('singer_name', song.singer_name)
        song.url_video = data.get('url_video', song.url_video)
        song.url_audio = data.get('url_audio', song.url_audio)
        song.image = data.get('image', song.image)

        song.save()
        return song
    except Song.DoesNotExist:
        return None
    except Song.MultipleObjectsReturned:
        return None

def delete_song_service(song_id):
    try:
        song = Song.objects.get(id=song_id)
        song.delete()
        return song
    except Song.DoesNotExist:
        return None
    except Song.MultipleObjectsReturned:
        return None
