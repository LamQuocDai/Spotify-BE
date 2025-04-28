from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import ObtainAuthToken
from .views import SongViewSet, GenreViewSet

router = DefaultRouter()
router.register(r'songs', SongViewSet, basename='song')
router.register(r'genres', GenreViewSet, basename='genre')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', ObtainAuthToken.as_view(), name='api_token_auth')
]
