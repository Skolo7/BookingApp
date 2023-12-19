from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib import messages
from django.db.models import Q
from ..models.products import Desk, Room, Parking
from ..models.reservations import Reservation
from ..forms import ReservationForm, ReserveDeskForm
from users.models import Account
from django.contrib.auth.mixins import LoginRequiredMixin


class ReservationListView(LoginRequiredMixin, View):
    template_name = 'reservations_template.html'


    def get(self, request, *args, **kwargs):
        reservations = Account.objects.all()
        return render(request, self.template_name, {'reservations': reservations})