from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class PasswordResetRequestForm(forms.Form):
    """
    Form for requesting password reset.
    """
    email = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )


class PasswordResetConfirmForm(forms.Form):
    """
    Form for setting new password.
    """
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match.")
        validate_password(password2)
        return password2