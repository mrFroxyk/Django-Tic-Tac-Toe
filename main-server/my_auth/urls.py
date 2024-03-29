from django.urls import path
from .views import *

app_name = 'my_auth'
urlpatterns = [
    path('', custom_login, name='login'),
    path('guest_login/', guest_login, name='guest_login'),
    path('singup/', signup, name='signup'),
    path('logout/', logout_user, name='logout')
]
