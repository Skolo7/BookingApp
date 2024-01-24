from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.contrib import messages
from django.db.models import Q
from ..models.products import Desk, Room, Parking
from ..models.reservations import Reservation
from ..forms import FilterAvailabilityForm, ReserveDeskForm
from users.models import Account
from django.contrib.auth.mixins import LoginRequiredMixin
from icecream import ic

class ReserveDeskView(LoginRequiredMixin, View):
    template_name = 'reserve.html'

    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        form = FilterAvailabilityForm()
        reservation_form = ReserveDeskForm()
        default_desks = self.get_default_desks(today)
        return self.render_with_form_and_default_desks(request, form, default_desks, today, reservation_form)

    def post(self, request, *args, **kwargs):
        form = ReserveDeskForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.person = self.request.user.id
            form.save()
            available_desks = self.get_filtered_desks(form)
            self.get(request, available_desks=available_desks)
        return self.get(request)

    def get_filtered_desks(self, form):
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        return self.get_available_desks(start_date=start_date, end_date=end_date)

    @staticmethod
    def get_default_desks(today):
        reservations_today = Reservation.objects.filter(start_date__range=(today, today)).select_related('desk')
        reserved_desks_today = {reserv.desk for reserv in reservations_today}
        all_desks = set(Desk.objects.all())
        return all_desks - reserved_desks_today

    # def render_with_desks(self, request, available_desks):
    #     context = {'all_desks': available_desks}
    #     return render(request, self.template_name, context=context)

    def render_with_form_and_default_desks(self, request, form, default_desks, today, reservation_form):
        context = {
            'all_desks': default_desks,
            'today': today,
            'form': form,
            'date_form': FilterAvailabilityForm(),
            'reservation_form': reservation_form
        }
        return render(request, self.template_name, context=context)

    def get_available_desks(self, start_date, end_date):
        available_desks = set(Desk.objects.all()) - {reserv.desk for reserv in
                                                     Reservation.objects.filter(
                                                         start_date__range=(start_date, end_date),
                                                         end_date__range=(start_date, end_date)).select_related(
                                                         'desk')}
        return available_desks