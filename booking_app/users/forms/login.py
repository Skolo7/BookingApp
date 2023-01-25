from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
    attrs={'placeholder': 'email',
           'class': 'form-control',
           'aria-label': 'Email',
           'aria-describedby': 'email-addon',

           }))
    password = forms.CharField(widget=forms.PasswordInput(
                               attrs={'placeholder': 'password',
           'class': 'form-control',
           'aria-label': 'Password',
           'aria-describedby': 'password-addon'
                                      }
                               ))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist!')
            if not user.is_active:
                raise forms.ValidationError('This user is not active!')
            return super(UserLoginForm, self).clean(*args, **kwargs)
