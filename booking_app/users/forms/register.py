from django import forms
from django.contrib.auth.forms import UserCreationForm
from ..models import Account



class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email']

    # def clean_password_confirmation(self):
    #     password = self.cleaned_data.get('password')
    #     password2 = self.cleaned_data.get('password2')
    #     if password != password2:
    #         raise forms.ValidationError('Passwords must match')
    #     return password
