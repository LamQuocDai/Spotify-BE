import json
import jwt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Spotify_BE import settings
from .services import (
    addSongToPlaylist,
    goToArtist,
    view_credits,
    getSongFromPlaylist,
    deleteSongFromPlaylist,
    searchSongFromPlaylist,
)
from ..utils.jwt_utils import decode_jwt_token
from ..utils.helper import get_token


@csrf_exempt
def add_song_to_playlist(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            playlist_id = data.get("playlist_id")
            song_id = data.get("song_id")

            if not all([playlist_id, song_id]):
                return JsonResponse(
                    {"status": "error", "message": "playlist_id, and song_id are required"},
                    status=400
                )

            # Sử dụng hàm chung để giải mã token
            user, payload, error_response = decode_jwt_token(get_token(request))
            if error_response:
                return error_response

            response = addSongToPlaylist(request, playlist_id, song_id, user.id)
            return response

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON data"}, status=400
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)}, status=500
            )

    return JsonResponse(
        {"status": "error", "message": "Method not allowed"}, status=405
    )


@csrf_exempt
def add_to_liked_songs_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Sử dụng hàm chung để giải mã token
            user, payload, error_response = decode_jwt_token(get_token(request))
            if error_response:
                return error_response  # Trả về lỗi nếu có

            song_id = data.get('song_id')

            # Thêm bài hát vào danh sách yêu thích
            response = addSongToPlaylist(request, None, song_id, user.id, is_liked_song=True)
            return response

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON data"}, status=400
            )
        except Exception as e:
            print("Unexpected error:", str(e))
            return JsonResponse(
                {"status": "error", "message": str(e)}, status=500
            )

    return JsonResponse(
        {"status": "error", "message": "Method not allowed"}, status=405
    )


@csrf_exempt
def getSongsFromPlaylist(request, playlist_id):
    if request.method == 'GET':
        try:
            # Sử dụng hàm chung để giải mã token
            user, payload, error_response = decode_jwt_token(get_token(request))
            if error_response:
                return error_response

            # Lấy danh sách bài hát từ playlist
            response = getSongFromPlaylist(playlist_id, user.id)
            return response

        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)}, status=500
            )

    return JsonResponse(
        {"status": "error", "message": "Method not allowed"}, status=405
    )


@csrf_exempt
def get_liked_songs_view(request):
    if request.method == 'GET':
        try:
            data = json.loads(request.body) if request.body else {}

            user, payload, error_response = decode_jwt_token(get_token(request))
            if error_response:
                return error_response  # Trả về lỗi nếu có

            response = getSongFromPlaylist(None, user.id, is_liked_song=True)
            return response

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON data"}, status=400
            )
        except Exception as e:
            print("Unexpected error:", str(e))
            return JsonResponse(
                {"status": "error", "message": str(e)}, status=500
            )

    return JsonResponse(
        {"status": "error", "message": "Method not allowed"}, status=405
    )


@csrf_exempt
def searchSongsFromPlaylist(request, playlist_id):
    if request.method == 'GET':
        try:
            data = json.loads(request.body) if request.body else {}

            # Sử dụng hàm chung để giải mã token
            user, payload, error_response = decode_jwt_token(get_token(request))
            if error_response:
                return error_response  # Trả về lỗi nếu có

            # Lấy query tìm kiếm
            query = request.GET.get('query', None)

            # Tìm kiếm bài hát trong playlist
            response = searchSongFromPlaylist(playlist_id, user.id, query)
            return response

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON data"}, status=400
            )
        except Exception as e:
            print("Unexpected error:", str(e))
            return JsonResponse(
                {"status": "error", "message": str(e)}, status=500
            )

    return JsonResponse(
        {"status": "error", "message": "Method not allowed"}, status=405
    )


@csrf_exempt
def search_liked_songs_view(request):
    if request.method == 'GET':
        try:
            user, payload, error_response = decode_jwt_token(get_token(request))
            if error_response:
                return error_response  # Trả về lỗi nếu có

            # Lấy query tìm kiếm
            query = request.GET.get('query', None)

            # Tìm kiếm bài hát trong danh sách yêu thích
            response = searchSongFromPlaylist(None, user.id, query, is_liked_song=True)
            return response

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON data"}, status=400
            )
        except Exception as e:
            print("Unexpected error:", str(e))
            return JsonResponse(
                {"status": "error", "message": str(e)}, status=500
            )

    return JsonResponse(
        {"status": "error", "message": "Method not allowed"}, status=405
    )


@csrf_exempt
def deleteSongFrom_Playlist(request, playlist_id, song_id):
    if request.method == 'DELETE':
        try:
            user, payload, error_response = decode_jwt_token(get_token(request))
            if error_response:
                return error_response

            response = deleteSongFromPlaylist(playlist_id, song_id, user.id)
            return response

        except Exception as e:
            return JsonResponse({"status": "error", "message": "Internal server error: " + str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)


@csrf_exempt
def remove_from_liked_songs_view(request, song_id):
    if request.method == 'DELETE':
        try:
            user, payload, error_response = decode_jwt_token(get_token(request))
            if error_response:
                return error_response  # Trả về lỗi nếu có

            # Xóa bài hát khỏi danh sách yêu thích
            response = deleteSongFromPlaylist(None, song_id, user.id, is_liked_song=True)
            return response

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON data"}, status=400
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)}, status=500
            )

    return JsonResponse(
        {"status": "error", "message": "Method not allowed"}, status=405
    )

@csrf_exempt
def go_to_artist(request, artist_id):
    if request.method == 'GET':
        try:
            # Sử dụng hàm chung để giải mã token
            user, payload, error_response = decode_jwt_token(get_token(request))
            if error_response:
                return error_response  # Trả về lỗi nếu có

            # Xem thông tin nghệ sĩ
            response = goToArtist(request, artist_id)
            return response

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON data"}, status=400
            )
        except Exception as e:
            print("Unexpected error:", str(e))
            return JsonResponse(
                {"status": "error", "message": str(e)}, status=500
            )

    return JsonResponse(
        {"status": "error", "message": "Method not allowed"}, status=405
    )

@csrf_exempt
def view_credits(request, song_id):
    if request.method == 'GET':
        try:
            # Sử dụng hàm chung để giải mã token
            user, payload, error_response = decode_jwt_token(get_token(request))
            if error_response:
                return error_response  # Trả về lỗi nếu có

            # Xem thông tin tín dụng bài hát
            response = view_credits(request, song_id)
            return response

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON data"}, status=400
            )
        except Exception as e:
            print("Unexpected error:", str(e))
            return JsonResponse(
                {"status": "error", "message": str(e)}, status=500
            )

    return JsonResponse(
        {"status": "error", "message": "Method not allowed"}, status=405
    )