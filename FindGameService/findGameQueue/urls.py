from django.urls import path
from .views import *

urlpatterns = [
    path('queue', Queue.as_view(), name='queue')
]
