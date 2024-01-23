from django.urls import path
from .views import CustomLoginView, guest_login

urlpatterns = [
    path('login', CustomLoginView.as_view(), name='login'),
    path('guest_login', guest_login, name='guest_login')
]
