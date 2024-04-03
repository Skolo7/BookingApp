from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm

from ..models import Account


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField()
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
