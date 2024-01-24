from django.urls import path
from .views import *

urlpatterns = [
    path('', online, name='online')
]
