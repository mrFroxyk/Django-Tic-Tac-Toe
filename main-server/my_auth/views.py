from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from .forms import AuthForm, RegisterUserForm
from .logic import GlobalIDUserManager
from .models import CustomUser

IDManager = GlobalIDUserManager()


def signup(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('my_auth:login'))
    context = {
        'form': RegisterUserForm(),
        'user': request.user,
    }
    return render(request, 'my_auth/signup.html', context)


class CustomLoginView(LoginView):
    form_class = AuthForm
    template_name = 'my_auth/login.html'

    def get_success_url(self):
        return reverse_lazy('chat:chat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        return context


def guest_login(request):
    if request.user.is_authenticated:
        return HttpResponse(f'You are authorization now, {request.user.username}')
    else:
        guest_id = IDManager.get_id_for_new_guest()
        guest_username = f'guest_{guest_id}'
        guest_user = CustomUser.objects.create(username=guest_username, is_quest=True)
        request.session.set_expiry(86400)
        login(request, guest_user)
        return HttpResponse(f'You were logged in under the nickname {request.user.username}')


def logout_user(request):
    logout(request)

