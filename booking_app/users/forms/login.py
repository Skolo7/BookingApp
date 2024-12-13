from django import forms
from django.contrib.auth.forms import AuthenticationForm

from ..models import Account


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', required=True, widget=forms.TextInput)
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ['username', 'password']
