from django.urls import path
from . import views


app_name = 'chat'

urlpatterns = [
    path('', views.get_chats, name='get_chats'),
    path('<int:chat_id>/', views.get_chat, name='get_chat'),
    path('create/', views.create_chat, name='create_chat'),
    path('<int:chat_id>/update/', views.update_chat, name='update_chat'),
    path('<int:chat_id>/delete/', views.delete_chat, name='delete_chat'),
]
