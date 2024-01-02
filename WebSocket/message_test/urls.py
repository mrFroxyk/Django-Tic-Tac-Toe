from django.urls import path
from .views import *

app_name = "message_test"
urlpatterns = [
    path("", index, name="index")
]
