from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class ProfileView(LoginRequiredMixin, View):
    template_name = 'users/profile.html'


def get(self, request, *args, **kwargs):
    return render(request, self.template_name)
