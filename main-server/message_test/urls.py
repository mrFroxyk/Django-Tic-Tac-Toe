from django.urls import path, re_path
from .views import *
from .consumers import SimpleMessageConsumer

app_name = "message_test"
urlpatterns = [
    path("", index, name="index")
]

websocket_urlpatterns = [
    re_path(r'ws', SimpleMessageConsumer.as_asgi(), name="websocket")
]
# print(websocket_urlpatterns)
