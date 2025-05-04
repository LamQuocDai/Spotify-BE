import jwt
from django.http import JsonResponse
from django.conf import settings
from ..users.models import User

def decode_jwt_token(token):
    if not token:
        return None, None, JsonResponse(
            {"status": "error", "message": "Token is required"}, status=400
        )

    try:
        # Giải mã token
        payload = jwt.decode(token, settings.SECRET_KEY_JWT, algorithms=["HS256"])
        user_id = payload.get("user_id")

        if not user_id:
            return None, None, JsonResponse(
                {"status": "error", "message": "Invalid token payload"}, status=400
            )

        # Lấy user từ database
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None, None, JsonResponse(
                {"status": "error", "message": "User not found"}, status=404
            )

        return user, payload, None

    except jwt.ExpiredSignatureError:
        return None, None, JsonResponse(
            {"status": "error", "message": "Token has expired"}, status=401
        )
    except jwt.InvalidTokenError as e:
        return None, None, JsonResponse(
            {"status": "error", "message": f"Invalid token: {str(e)}"}, status=401
        )