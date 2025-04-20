from django.urls import path
from .views import create_user, get_user, get_users, update_user, delete_user

urlpatterns = [
    path('', get_users, name='get_users'),
    path('<int:user_id>/', get_user, name='get_user'),
    path('create/', create_user, name='create_user'),
    path('<int:user_id>/update/', update_user, name='update_user'),
    path('<int:user_id>/delete/', delete_user, name='delete_user'),
]