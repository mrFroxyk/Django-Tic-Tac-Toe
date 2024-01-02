"""
ASGI config for WebSocket project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
from django.core.asgi import get_asgi_application
from django.urls import include, path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
# from ...WebSocket.message_test.urls import websocket_urlpatterns

from .consumers import SimpleMessageConsumer
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebSocket.settings')

django_asgi_application = get_asgi_application()
# print(include('message_test.routing'))
application = ProtocolTypeRouter(
    {
        'http': django_asgi_application,
        'websocket': AuthMiddlewareStack(
            URLRouter([
                path(r'ws', SimpleMessageConsumer.as_asgi(), name='ws'),
                # path(r'ws2', include('message_test.routing'))
                # 'ws/', include('message_test.urls')
            ])
        )
    }
)
