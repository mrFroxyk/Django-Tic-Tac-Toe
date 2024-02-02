from django.shortcuts import redirect
from django.urls import reverse


class AuthCheckerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path == reverse('my_auth:login'):
            return response
        if not request.user.is_authenticated:
            return redirect(reverse('my_auth:login'))
        return response
