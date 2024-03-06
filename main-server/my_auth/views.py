from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
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


def custom_login(request):
    if request.method == 'POST':
        form = AuthForm(request, data=request.POST)
        if form.is_valid():
            next_url = request.POST.get('next')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect(next_url)
    else:
        form = AuthForm()

    context = {
        'form': form,
        'next': request.GET.get('next'),
    }
    return render(request, 'my_auth/login.html', context)


def guest_login(request):
    if request.user.is_authenticated:
        return HttpResponse(f'You are authorization now, {request.user.username}')
    else:
        guest_id = IDManager.get_id_for_new_guest()
        guest_username = f'guest_{guest_id}'
        guest_user = CustomUser.objects.create(username=guest_username, is_quest=True)
        request.session.set_expiry(86400)
        login(request, guest_user)
        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        else:
            return HttpResponse(f'You were logged in under the nickname {request.user.username}')


def logout_user(request):
    logout(request)
    return redirect('my_auth:login')
