from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from ..models.reservations import Reservation


class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'user_reservations.html'
    context_object_name = 'reservations'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(person=self.request.user).order_by('-start_date')


