from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from ..models import Account

# User = get_user_model()


class UserLoginForm(AuthenticationForm):
    # def __init__(self, *args, **kwargs):
    #     super(UserLoginForm, self).__init__(*args, **kwargs)
    email = forms.EmailField()
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    # password = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "placeholder": "password",
    #             "class": "form-control",
    #             "aria-label": "Password",
    #             "aria-describedby": "password-addon",
    #         }
    #     )
    # )
    #
    # def clean(self, *args, **kwargs):
    #     email = self.cleaned_data.get("email")
    #
