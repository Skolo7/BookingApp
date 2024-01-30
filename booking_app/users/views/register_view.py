from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from ..forms import UserRegistrationForm
from ..models import Account
from django.views import View
from django.contrib.auth.forms import UserCreationForm

import logging

logger = logging.getLogger(__name__)

class RegisterView(View):
    template_name = 'users/register.html'
    form_class = UserRegistrationForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = Account.objects.create_user(username=email, password=password)
            user.save()
            messages.success(request, 'Account was created for {}'.format(email))
            return redirect('login')

        return render(request, self.template_name, {'form': form})