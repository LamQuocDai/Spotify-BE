# apps/users/urls.py
from django.urls import path
from .views import RegisterView, LoginView, SocialLoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('social-login/', SocialLoginView.as_view(), name='social-login'),
]