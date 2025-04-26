from django.urls import path
from .views import ConversationList, MessageList

urlpatterns = [
    path('chats/', ConversationList.as_view(), name='conversation-list'),
    path('chats/<int:other_user_id>/messages/', MessageList.as_view(), name='message-list'),
]