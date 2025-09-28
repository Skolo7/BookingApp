from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from ..forms import AccountForm
from ..models import Account


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return get_object_or_404(Account, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = AccountForm(self.request.POST, instance=self.request.user)
        else:
            context['form'] = AccountForm(instance=self.request.user)

        return context

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        else:
            return self.form_invalid(form)
        
        return super().form_valid(form)
