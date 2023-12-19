from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from ..forms import UserLoginForm, UserRegistrationForm
from ..models import Account
from django.views import View
from django.contrib.auth.forms import UserCreationForm
import logging

logger = logging.getLogger(__name__)

class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('login'))