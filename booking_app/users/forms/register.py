from django import forms
from django.contrib.auth.forms import UserCreationForm
from ..models import Account


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email"]
