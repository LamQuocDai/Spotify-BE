from django.urls import path
from apps.chat.views import create_chat, get_chat, get_chats, update_chat, delete_chat

urlpatterns = [
    path('', get_chats, name='get_chats'),
    path('<int:chat_id>/', get_chat, name='get_chat'),
    path('create/', create_chat, name='create_chat'),
    path('<int:chat_id>/update/', update_chat, name='update_chat'),
    path('<int:chat_id>/delete/', delete_chat, name='delete_chat'),
]