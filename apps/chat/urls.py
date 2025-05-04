from django.urls import path
from .views import ConversationList, MessageList, SearchUsers

urlpatterns = [
    path('chats/', ConversationList.as_view(), name='conversation-list'),
    path('chats/<str:other_user_id>/messages/', MessageList.as_view(), name='message-list'),
    path('chats/users/search/', SearchUsers.as_view(), name='search_users')
]