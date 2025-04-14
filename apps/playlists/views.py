from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
import json
from apps.utils.response import success_response, error_response
from . import services

@csrf_exempt
def create_playlist(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            playlist = services.create_playlist_service(data)
            playlist_json = json.loads(serialize('json', [playlist]))[0]['fields']

            return success_response("Create playlist success",playlist_json)
        except Exception as e:
            return error_response(e.__str__())


def get_playlists(request):
    if request.method == 'GET':
        try:
            playlists = services.get_playlists_service()
            return success_response("Get list success",playlists)
        except Exception as e:
            return error_response(e.__str__())

def get_playlist(request, playlist_id):
    if request.method == 'GET':
        try:
            playlist = services.get_playlist_service(playlist_id)
            if playlist is None:
                return error_response("Playlist doesn't exist")
            playlist_json = json.loads(serialize('json', [playlist]))[0]['fields']
            return success_response("Get playlist success",playlist_json)
        except Exception as e:
            return error_response(e.__str__())

@csrf_exempt
def update_playlist(request, playlist_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            playlist = services.update_playlist_service(playlist_id,data)
            if playlist is None:
                return error_response("Playlist doesn't exist")
            playlist_json = json.loads(serialize('json', [playlist]))[0]['fields']
            return success_response("Update playlist success",playlist_json)
        except Exception as e:
            return error_response(e.__str__())

@csrf_exempt
def delete_playlist(request, playlist_id):
    if request.method == 'DELETE':
        try:
            playlist = services.get_playlist_service(playlist_id)
            if playlist is None:
                return error_response("Playlist doesn't exist")
            playlist_delete = services.delete_playlist_service(playlist_id)
            playlist_json = json.loads(serialize('json', [playlist_delete]))[0]['fields']
            return success_response("Delete playlist success",playlist_json)
        except Exception as e:
            return error_response(e.__str__())