import logging
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from ..forms import UserLoginForm

logger = logging.getLogger(__name__)


class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        logger.info(f"logging user: {username}")

        user = authenticate(request=self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            logger.info(f"{username} logged in successfully")
            return super().form_valid(form)
        else:
            logger.warning(f"failed to log in user{username}")
            messages.error(self.request, 'Invalid Login or Password')
            return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):
        logger.warning(f"invalid login form {form.errors}")
        messages.error(self.request, 'Invalid Login or Password')
        return super().form_invalid(form)
