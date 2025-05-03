"""
ASGI config for Spotify_BE project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Spotify_BE.settings")

# Setup Django - this is the crucial line that's missing
django.setup()

# Now import after Django is fully set up
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import apps.chat.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            apps.chat.routing.websocket_urlpatterns
        )
    ),
})