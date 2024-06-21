from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from ..models.reservations import Reservation


class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'reservations_template.html'
    context_object_name = 'reservations'

