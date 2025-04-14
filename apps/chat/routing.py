from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<int:receiver_id>/', consumers.PrivateChatConsumer.as_asgi()),
]