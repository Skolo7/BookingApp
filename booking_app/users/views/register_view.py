import logging

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from ..forms import UserRegistrationForm

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
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            form.save()
            messages.success(
                request,
                f"Account was created for {form.cleaned_data['username']}",
            )
            logger.info(f"New user account: {username} ({email})")
            return redirect('login')
        else:
            logger.warning(f"Failed registration attempt: {form.errors}")
        return render(request, self.template_name, {'form': form})
