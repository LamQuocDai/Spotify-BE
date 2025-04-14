from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
import json
from apps.utils.response import success_response, error_response
from . import services
@csrf_exempt
def create_genre(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            genre = services.create_genre_service(data)
            genre_json = json.loads(serialize('json', [genre]))[0]['fields']

            return success_response("Create genre success",genre_json)
        except Exception as e:
            return error_response(e.__str__())


def get_genres(request):
    if request.method == 'GET':
        try:
            genres = services.get_genres_service()
            return success_response("Get list success",genres)
        except Exception as e:
            return error_response(e.__str__())

def get_genre(request, genre_id):
    if request.method == 'GET':
        try:
            genre = services.get_genre_service(genre_id)
            if genre is None:
                return error_response("Genre doesn't exist")
            genre_json = json.loads(serialize('json', [genre]))[0]['fields']
            return success_response("Get genre success",genre_json)
        except Exception as e:
            return error_response(e.__str__())

@csrf_exempt
def update_genre(request, genre_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            genre = services.update_genre_service(genre_id,data)
            if genre is None:
                return error_response("Genre doesn't exist")
            genre_json = json.loads(serialize('json', [genre]))[0]['fields']
            return success_response("Update genre success",genre_json)
        except Exception as e:
            return error_response(e.__str__())

@csrf_exempt
def delete_genre(request, genre_id):
    if request.method == 'DELETE':
        try:
            genre = services.get_genre_service(genre_id)
            if genre is None:
                return error_response("Genre doesn't exist")
            genre_delete = services.delete_genre_service(genre_id)
            genre_json = json.loads(serialize('json', [genre_delete]))[0]['fields']
            return success_response("Delete genre success",genre_json)
        except Exception as e:
            return error_response(e.__str__())

@csrf_exempt
def create_song(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            song = services.create_song_service(data)
            song_json = json.loads(serialize('json', [song]))[0]['fields']

            return success_response("Create song success",song_json)
        except Exception as e:
            return error_response(e.__str__())


def get_songs(request):
    if request.method == 'GET':
        try:
            songs = services.get_songs_service()
            return success_response("Get list success",songs)
        except Exception as e:
            return error_response(e.__str__())

def get_song(request, song_id):
    if request.method == 'GET':
        try:
            song = services.get_song_service(song_id)
            if song is None:
                return error_response("Song doesn't exist")
            song_json = json.loads(serialize('json', [song]))[0]['fields']
            return success_response("Get song success",song_json)
        except Exception as e:
            return error_response(e.__str__())

@csrf_exempt
def update_song(request, song_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            song = services.update_song_service(song_id,data)
            if song is None:
                return error_response("Song doesn't exist")
            song_json = json.loads(serialize('json', [song]))[0]['fields']
            return success_response("Update song success",song_json)
        except Exception as e:
            return error_response(e.__str__())

@csrf_exempt
def delete_song(request, song_id):
    if request.method == 'DELETE':
        try:
            song = services.get_song_service(song_id)
            if song is None:
                return error_response("Song doesn't exist")
            song_delete = services.delete_song_service(song_id)
            song_json = json.loads(serialize('json', [song_delete]))[0]['fields']
            return success_response("Delete song success",song_json)
        except Exception as e:
            return error_response(e.__str__())