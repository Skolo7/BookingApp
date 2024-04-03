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


class ReservationListView(LoginRequiredMixin, View):
    template_name = 'reservations_template.html'

    def get(self, request, *args, **kwargs):
        reservations = Reservation.objects.all()
        #
        # reservations_data = []
        #
        # for reservation in reservations:
        #     person_name = reservation.person.name
        #     start_date_sample = reservation.start_date
        #     end_date_sample = reservation.end_date
        #     reserv_type = reservation.type
        #     reservations_data.append({'reservation': reservation, 'person_name': person_name, 'start_date_sample': start_date_sample, 'end_date_sample': end_date_sample, 'reserv_type': reserv_type})

        return render(request, self.template_name, {'reservations': reservations})
