from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegistrationForm


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'users/login.html', {'form': form})


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        new_user.set_password(password)
        new_user.save()
        login(request, new_user)
        return redirect('home')
    return render(request, 'users/register.html', {'form': form})