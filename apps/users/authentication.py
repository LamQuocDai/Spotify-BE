# apps/users/authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from Spotify_BE import settings

class CustomJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        validated_token = super().get_validated_token(raw_token)
        # Kiểm tra xem token có được ký bằng SECRET_KEY_JWT không
        # Simple JWT tự động kiểm tra chữ ký, nên không cần thêm logic ở đây
        return validated_token