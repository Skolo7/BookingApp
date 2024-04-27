import logging

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View


logger = logging.getLogger(__name__)


class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('login'))
