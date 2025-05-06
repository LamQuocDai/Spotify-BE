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
    get_all_playlists,
    search_all_playlists
)
from ..utils.jwt_utils import decode_jwt_token
from ..utils.helper import get_token
# ------------------------------------- Views --------------------------------------

@csrf_exempt
def createPlaylist(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Sử dụng hàm chung để giải mã token
            user, payload, error_response = decode_jwt_token(get_token(request))
            if error_response:
                return error_response  # Trả về lỗi nếu có

            print("Payload:", payload)

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
            data = json.loads(request.body)

            # Sử dụng hàm chung để giải mã token
            user, payload, error_response = decode_jwt_token(get_token(request))
            if error_response:
                return error_response

            try:
                playlist = Playlist.objects.get(id=id)
            except Playlist.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Playlist not found"}, status=404)

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
            user, payload, error_response = decode_jwt_token(get_token(request))
            if error_response:
                return error_response

            try:
                playlist = Playlist.objects.get(id=id)
            except Playlist.DoesNotExist:
                return JsonResponse(
                    {"status": "error", "message": "Playlist not found"}, status=404
                )

            response = delete_playlist(playlist, user)
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
            user, payload, error_response = decode_jwt_token(get_token(request))
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

    return JsonResponse(
        {"status": "error", "message": "Method not allowed"}, status=405
    )

@csrf_exempt
def getPlaylists(request):
    if request.method == "GET":
        try:
            page = request.GET.get("page", "1")
            page_size = request.GET.get("page_size", "10")

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
    if request.method == "GET":
        try:
            query = request.GET.get("q", "")
            page = request.GET.get("page", "1")
            page_size = request.GET.get("page_size", "10")

            user, payload, error_response = decode_jwt_token(get_token(request))
            if error_response:
                return error_response

            response = search_playlists(user, query, page, page_size)
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
def searchPlaylists(request):
    if request.method == "GET":
        try:
            query = request.GET.get("q", "")
            page = request.GET.get("page", "1")
            page_size = request.GET.get("page_size", "10")

            user, payload, error_response = decode_jwt_token(get_token(request))
            if error_response:
                print("Token decode error:", error_response)
                return error_response

            print("Payload:", payload)

            response = search_playlists(user, query, page, page_size)  # User-specific search
            print("Search playlists response:", response)
            return response

        except json.JSONDecodeError:
            print("JSON decode error")
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON data"}, status=400
            )
        except Exception as e:
            print("Unexpected error in searchPlaylists:", str(e))
            return JsonResponse(
                {"status": "error", "message": "Internal server error: " + str(e)}, status=500
            )

    print("Method not allowed")
    return JsonResponse(
        {"status": "error", "message": "Method not allowed"}, status=405
    )

@csrf_exempt
def searchAllPlaylists(request):
    if request.method == "GET":
        try:
            query = request.GET.get("q", "")
            page = request.GET.get("page", "1")
            page_size = request.GET.get("page_size", "10")

            user, payload, error_response = decode_jwt_token(get_token(request))
            if error_response:
                return error_response

            is_admin = user.groups.filter(name__in=['admin', 'full_role']).exists()
            if not is_admin:
                return JsonResponse(
                    {"status": "error", "message": "Permission denied"}, status=403
                )

            response = search_all_playlists(query, page, page_size)  # Global search
            return response

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON data"}, status=400
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": "Internal server error: " + str(e)}, status=500
            )

    return JsonResponse(
        {"status": "error", "message": "Method not allowed"}, status=405
    )