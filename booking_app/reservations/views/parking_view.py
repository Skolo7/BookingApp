from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib import messages
from django.db.models import Q
from ..models.products import Desk, Room, Parking
from ..models.reservations import Reservation
from ..forms import ReserveDeskForm
from users.models import Account
from django.contrib.auth.mixins import LoginRequiredMixin


class ParkingView(LoginRequiredMixin, View):
    template_name = 'parking.html'

    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        form = ReservationForm()
        default_parkings = self.get_default_parkings(today)
        return self.render_with_form_and_default_parkings(request, form, default_parkings, today)

    def post(self, request, *args, **kwargs):
        form = ReservationForm(request.POST)
        if form.is_valid():
            available_parkings = self.get_filtered_parkings(form)
            return self.render_with_parkings(request, available_parkings)
        return self.get(request)

    def get_filtered_parkings(self, form):
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        return get_available_parkings(start_date=start_date, end_date=end_date)

    def get_default_parkings(self, today):
        reservations_today = Reservation.objects.filter(start_date__range=(today, today)).select_related('parking')
        reserved_parkings_today = {reserv.parking for reserv in reservations_today}
        all_parkings = set(Parking.objects.all())
        return all_parkings - reserved_parkings_today

    def render_with_parkings(self, request, available_parkings):
        context = {'all_parkings': available_parkings}
        return render(request, self.template_name, context=context)

    def render_with_form_and_default_parkings(self, request, form, default_parkings, today):
        context = {
            'all_parkings': default_parkings,
            'today': today,
            'form': form,
            'date_form': ReservationForm()
        }
        return render(request, self.template_name, context=context)
