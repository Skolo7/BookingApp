from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model
from users.services.password_reset import (
    send_password_reset_link,
    validate_password_reset_token,
    invalidate_password_reset_token
)
from users.forms import PasswordResetRequestForm, PasswordResetConfirmForm

User = get_user_model()


class PasswordResetRequestView(View):
    """
    View for requesting password reset.
    """
    template_name = 'users/password_reset_form.html'
    
    def get(self, request):
        form = PasswordResetRequestForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            success = send_password_reset_link(request, email)
            
            messages.success(
                request,
                'If an account with this email exists, '
                'you will receive password reset instructions.'
            )
            return redirect('password_reset_done_custom')
        
        return render(request, self.template_name, {'form': form})


class PasswordResetConfirmView(View):
    """
    View for setting new password.
    """
    template_name = 'users/password_reset_confirm.html'
    
    def get(self, request, token):
        user_data = validate_password_reset_token(token)
        if not user_data:
            messages.error(request, 'The password reset link is invalid or has expired.')
            return redirect('password_reset_request_custom')
        
        form = PasswordResetConfirmForm()
        return render(request, self.template_name, {'form': form, 'token': token})
    
    def post(self, request, token):
        user_data = validate_password_reset_token(token)
        if not user_data:
            messages.error(request, 'The password reset link is invalid or has expired.')
            return redirect('password_reset_request_custom')
        
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(id=user_data['user_id'])
                user.set_password(form.cleaned_data['new_password1'])
                user.save()
                
                invalidate_password_reset_token(token)
                
                messages.success(request, 'Password has been successfully changed. You can now log in.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'An error occurred. User does not exist.')
                return redirect('password_reset_request_custom')
        
        return render(request, self.template_name, {'form': form, 'token': token})


class PasswordResetDoneCustomView(View):
    """
    View after sending reset link.
    """
    template_name = 'users/password_reset_done.html'
    
    def get(self, request):
        return render(request, self.template_name)


class PasswordResetCompleteCustomView(View):
    """
    View after successful password reset.
    """
    template_name = 'users/password_reset_complete.html'
    
    def get(self, request):
        return render(request, self.template_name)