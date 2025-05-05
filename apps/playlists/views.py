import jwt
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Spotify_BE import settings
from apps.users.models import User
from .models import Playlist
from .services import (
    create_playlist,
    update_playlist,
    delete_playlist,
    get_playlist,
    get_user_playlists,
    search_playlists,
    get_all_playlists
)
from ..utils.jwt_utils import decode_jwt_token


@csrf_exempt
def createPlaylist(request):
    if request.method == "POST":
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

            # Tạo playlist
            playlist, response = create_playlist(data, user)
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
def updatePlaylist(request, id):
    if request.method == "PUT":
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

            # Kiểm tra playlist tồn tại
            try:
                playlist = Playlist.objects.get(id=id)
            except Playlist.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Playlist not found"}, status=404)
            
            print(playlist)
            print(data)
            # Cập nhật playlist
            response = update_playlist(playlist, data, user)
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
def deletePlaylist(request, id):
    if request.method == "DELETE":
        try:
            token = request.GET.get("token")

            user, payload, error_response = decode_jwt_token(token)
            if error_response:
                return error_response

            try:
                playlist = Playlist.objects.get(id=id)
            except Playlist.DoesNotExist:
                print("Playlist not found:", id)
                return JsonResponse(
                    {"status": "error", "message": "Playlist not found"}, status=404
                )

            response = delete_playlist(playlist, user)
            print("Delete response:", response)
            return response

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON data"}, status=400
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": "Internal server error"}, status=500
            )

    return JsonResponse(
        {"status": "error", "message": "Method not allowed"}, status=405
    )


@csrf_exempt
def getPlaylist(request, id):
    if request.method == "GET":
        try:
            token = request.GET.get("token")

            user, payload, error_response = decode_jwt_token(token)
            if error_response:
                return error_response

            try:
                playlist = Playlist.objects.get(id=id)
            except Playlist.DoesNotExist:
                return JsonResponse(
                    {"status": "error", "message": "Playlist not found"}, status=404
                )

            response = get_playlist(playlist, user)
            return response

        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": "Internal server error: " + str(e)}, status=500
            )

    print("Method not allowed")
    return JsonResponse(
        {"status": "error", "message": "Method not allowed"}, status=405
    )

@csrf_exempt
def getPlaylists(request):
    if request.method == "GET":
        try:
            page = request.GET.get("page", "1")
            page_size = request.GET.get("page_size", "10")
            token = request.GET.get("token")

            user, payload, error_response = decode_jwt_token(token)
            if error_response:
                return error_response


            response = get_all_playlists(page, page_size)
            return response

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON data"}, status=400
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": "Internal server error"}, status=500
            )

    return JsonResponse(
        {"status": "error", "message": "Method not allowed"}, status=405
    )


@csrf_exempt
def getUserPlaylists(request, id):
    if request.method == "GET":
        try:
            user = User.objects.get(id=id)

            # Lấy danh sách playlists của user
            response = get_user_playlists(user)
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
def searchPlaylists(request):
    print("Entering searchPlaylists view")
    if request.method == "GET":
        try:
            query = request.GET.get("q", "")
            page = request.GET.get("page", "1")
            page_size = request.GET.get("page_size", "10")
            token = request.GET.get("token")

            # Decode JWT token
            if not token:
                return JsonResponse(
                    {"status": "error", "message": "Token is required"},
                    status=401
                )
            user, payload, error_response = decode_jwt_token(token)
            if error_response:
                print("Token decode error:", error_response)
                return error_response


            response = search_playlists(user, query, page, page_size)
            return response

        except json.JSONDecodeError:
            print("JSON decode error")
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON data"}, status=400
            )
        except Exception as e:
            print("Unexpected error in searchPlaylists:", str(e))
            return JsonResponse(
                {"status": "error", "message": "Internal server error"}, status=500
            )

    print("Method not allowed")
    return JsonResponse(
        {"status": "error", "message": "Method not allowed"}, status=405
    )