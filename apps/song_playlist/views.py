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


@csrf_exempt
def add_song_to_playlist(request):
    if request.method == 'POST':
        try:
            print("Request body:", request.body)
            data = json.loads(request.body)
            print("Parsed data:", data)
            token = data.get("token")
            print("Token:", token)

            # Sử dụng hàm chung để giải mã token
            user, payload, error_response = decode_jwt_token(token)
            if error_response:
                return error_response  # Trả về lỗi nếu có

            print("Payload:", payload)

            playlist_id = data.get('playlist_id')
            song_id = data.get('song_id')

            # Thêm bài hát vào playlist
            response = addSongToPlaylist(request, playlist_id, song_id)
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
def add_to_liked_songs_view(request):
    if request.method == 'POST':
        try:
            print("Request body:", request.body)
            data = json.loads(request.body)
            print("Parsed data:", data)
            token = data.get("token")
            print("Token:", token)

            # Sử dụng hàm chung để giải mã token
            user, payload, error_response = decode_jwt_token(token)
            if error_response:
                return error_response  # Trả về lỗi nếu có

            print("Payload:", payload)

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
            print("Request body:", request.body)
            data = json.loads(request.body) if request.body else {}
            print("Parsed data:", data)
            token = request.GET.get("token") or data.get("token")
            print("Token:", token)

            # Sử dụng hàm chung để giải mã token
            user, payload, error_response = decode_jwt_token(token)
            if error_response:
                return error_response  # Trả về lỗi nếu có

            print("Payload:", payload)

            # Lấy danh sách bài hát từ playlist
            response = getSongFromPlaylist(playlist_id, user.id)
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
def get_liked_songs_view(request):
    if request.method == 'GET':
        try:
            print("Request body:", request.body)
            data = json.loads(request.body) if request.body else {}
            print("Parsed data:", data)
            token = request.GET.get("token") or data.get("token")
            print("Token:", token)

            # Sử dụng hàm chung để giải mã token
            user, payload, error_response = decode_jwt_token(token)
            if error_response:
                return error_response  # Trả về lỗi nếu có

            print("Payload:", payload)

            # Lấy danh sách bài hát yêu thích
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
            print("Request body:", request.body)
            data = json.loads(request.body) if request.body else {}
            print("Parsed data:", data)
            token = request.GET.get("token") or data.get("token")
            print("Token:", token)

            # Sử dụng hàm chung để giải mã token
            user, payload, error_response = decode_jwt_token(token)
            if error_response:
                return error_response  # Trả về lỗi nếu có

            print("Payload:", payload)

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
            print("Request body:", request.body)
            data = json.loads(request.body) if request.body else {}
            print("Parsed data:", data)
            token = request.GET.get("token") or data.get("token")
            print("Token:", token)

            # Sử dụng hàm chung để giải mã token
            user, payload, error_response = decode_jwt_token(token)
            if error_response:
                return error_response  # Trả về lỗi nếu có

            print("Payload:", payload)

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
            print("Request body:", request.body)
            data = json.loads(request.body) if request.body else {}
            print("Parsed data:", data)
            token = data.get("token")
            print("Token:", token)

            # Sử dụng hàm chung để giải mã token
            user, payload, error_response = decode_jwt_token(token)
            if error_response:
                return error_response  # Trả về lỗi nếu có

            print("Payload:", payload)

            # Xóa bài hát khỏi playlist
            response = deleteSongFromPlaylist(playlist_id, song_id, user.id)
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
def remove_from_liked_songs_view(request, song_id):
    if request.method == 'DELETE':
        try:
            print("Request body:", request.body)
            data = json.loads(request.body) if request.body else {}
            print("Parsed data:", data)
            token = data.get("token")
            print("Token:", token)

            # Sử dụng hàm chung để giải mã token
            user, payload, error_response = decode_jwt_token(token)
            if error_response:
                return error_response  # Trả về lỗi nếu có

            print("Payload:", payload)

            # Xóa bài hát khỏi danh sách yêu thích
            response = deleteSongFromPlaylist(None, song_id, user.id, is_liked_song=True)
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
def go_to_artist(request, artist_id):
    if request.method == 'GET':
        try:
            print("Request body:", request.body)
            data = json.loads(request.body) if request.body else {}
            print("Parsed data:", data)
            token = request.GET.get("token") or data.get("token")
            print("Token:", token)

            # Sử dụng hàm chung để giải mã token
            user, payload, error_response = decode_jwt_token(token)
            if error_response:
                return error_response  # Trả về lỗi nếu có

            print("Payload:", payload)

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
            print("Request body:", request.body)
            data = json.loads(request.body) if request.body else {}
            print("Parsed data:", data)
            token = request.GET.get("token") or data.get("token")
            print("Token:", token)

            # Sử dụng hàm chung để giải mã token
            user, payload, error_response = decode_jwt_token(token)
            if error_response:
                return error_response  # Trả về lỗi nếu có

            print("Payload:", payload)

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