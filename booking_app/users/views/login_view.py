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

class LoginView(View): # FormView
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
        else:
            messages.error(request, 'Invalid Login or Password')

        context = {'form': form}
        return render(request, self.template_name, context)