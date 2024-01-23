from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.contrib.auth.forms import AuthenticationForm, BaseUserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy


class AuthForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class CustomLoginView(LoginView):
    form_class = AuthForm
    template_name = 'my_auth/reg.html'

    def get_success_url(self):
        return reverse_lazy('chat:chat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        return context


def guest_login(request):
    return HttpResponse('redirect to guest login')
# def login(request):
#     if request.method == 'POST':
#         form = AuthForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
