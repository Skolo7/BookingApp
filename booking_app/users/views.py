from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .forms import UserLoginForm, UserRegistrationForm
from .models import Account
import logging

logger = logging.getLogger(__name__)
# TODO REFACTOR. CLASS BASED VIEW.

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password1')
            logger.info('Account successfully created')
            user = Account.objects.create_user(password=password, username=email)
            user.save()
            messages.success(request, 'Account was Created for ')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        login(request, user)
        return redirect('index')

    context = {"form": UserLoginForm}
    return render(request, 'users/login.html', context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')