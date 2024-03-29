"""
ASGI config for Core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from game.urls import websocket_urlpatterns_game
from message_test.urls import websocket_urlpatterns
from chat.urls import websocket_urlpatterns_chat
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Core.settings')
django_asgi_application = get_asgi_application()
application = ProtocolTypeRouter(
    {
        'http': django_asgi_application,
        'websocket': AuthMiddlewareStack(
            URLRouter([
                *websocket_urlpatterns_game, *websocket_urlpatterns,
                *websocket_urlpatterns_chat,
            ])
        )
    }
)
