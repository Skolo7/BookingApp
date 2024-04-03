from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from users.models import Account

from ..forms import ReserveForm
from ..models.products import Desk, Parking, Room
from ..models.reservations import Reservation


class IndexView(LoginRequiredMixin, View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
