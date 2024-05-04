from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from .forms import UserProfileForm
from .models import UserProfile


class UserProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        user, created = UserProfile.objects.get_or_create(user=self.request.user)
        return user

    def get_success_url(self):
        return reverse_lazy('')
