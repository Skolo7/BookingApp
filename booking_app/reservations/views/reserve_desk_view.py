import datetime
from typing import Any
from urllib.parse import urlencode


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from icecream import ic

from ..forms import FilterAvailabilityForm, ReserveForm
from ..models.products import Desk, Room
from ..models.reservations import Reservation


# class FilterDeskView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         form = FilterAvailabilityForm(request.POST)
#         if form.is_valid():
#             start_date = form.cleaned_data['start_date']
#             end_date = form.cleaned_data['end_date']
#             start_date_param = start_date.strftime("%Y-%m-%d")
#             end_date_param = end_date.strftime("%Y-%m-%d")

#             url = reverse('reserve')
#             query_params = f'?start_date={start_date_param}&end_date={end_date_param}'

#             return redirect(f'{url}{query_params}')
#         else:
#             messages.error(request, "form is incorrect")
#             return redirect(reverse('reserve'))



class FilterDeskView(LoginRequiredMixin, View):
    DATE_FORMAT = "%Y-%m-%d"
    
    def post(self, request: Any, *args: Any, **kwargs: Any) -> HttpResponse:
        form = FilterAvailabilityForm(request.POST)
        
        if not form.is_valid():
            messages.error(request, "Invalid date range selection.")
            return redirect(reverse('reserve'))
            
        query_params = self._get_date_query_params(form.cleaned_data)
        return redirect(f"{reverse('reserve')}?{query_params}")
    
    def _get_date_query_params(self, cleaned_data: dict) -> str:
        params = {
            'start_date': cleaned_data['start_date'].strftime(self.DATE_FORMAT),
            'end_date': cleaned_data['end_date'].strftime(self.DATE_FORMAT)
        }
        return urlencode(params)


class ReserveDeskView(LoginRequiredMixin, View):
    template_name = 'reserve.html'

    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        reservation_form = ReserveForm()

        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        if start_date_str and end_date_str:
            start_date = timezone.datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = timezone.datetime.strptime(end_date_str, "%Y-%m-%d").date()
            if start_date < today or end_date < today:
                messages.error(request, 'Cannot reserve for past days.')
                return redirect('reserve_desk')
            available_desks = self.get_available_desks(start_date, end_date)
            available_rooms = self.get_available_rooms(start_date, end_date)
        else:
            ic()
            available_desks = self.get_default_desks(today)
            available_rooms = self.get_default_rooms(today)
        return self.render_with_form_and_desks(
            request, available_desks, available_rooms, today, reservation_form
        )

    def post(self, request, *args, **kwargs):
        form = ReserveForm(request.POST)
        today = timezone.now().date()

        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.person = self.request.user
            number, reservation_type = form.data['number'], form.data['type'].upper()

            if reservation.start_date < today or reservation.end_date < today:
                messages.error(request, "Cannot reserve for past days.")
                return self.get(request)

            if reservation_type == 'ROOM':
                reservation.room = Room.objects.get(number=number)
                reservation.type = 'ROOM'
            elif reservation_type == 'DESK':
                reservation.desk = Desk.objects.get(number=number)
                reservation.type = 'DESK'

            reservation.save()
            messages.success(request, 'Reservation confirmed.')
        else:
            messages.error(request, 'Reservation failure.')
        return self.get(request)

    @staticmethod
    def get_default_desks(today: datetime.datetime) -> set[Desk]:
        reservations_today = Reservation.objects.filter(
            start_date__range=(today, today)
        ).select_related('desk')
        reserved_desks_today = {reservation.desk for reservation in reservations_today}
        all_desks = set(Desk.objects.all())
        return all_desks - reserved_desks_today

    def render_with_form_and_desks(
        self, request, desks, rooms, today, reservation_form
    ) -> HttpResponse:
        context = {
            'all_desks': desks,
            'all_rooms': rooms,
            'today': today,
            'filter_form': FilterAvailabilityForm(),
            'reservation_form': reservation_form,
        }
        return render(request, self.template_name, context=context)

    def get_filtered_desks(self, form: ReserveForm) -> set[Desk]:
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        return self.get_available_desks(start_date=start_date, end_date=end_date)

    def get_available_desks(self, start_date, end_date) -> set[Desk]:
        available_desks = set(Desk.objects.all()) - {
            reservation.desk
            for reservation in Reservation.objects.filter(
                start_date__range=(start_date, end_date),
                end_date__range=(start_date, end_date),
            ).select_related('desk')
        }
        return available_desks

    def get_available_rooms(
        self, start_date: datetime.datetime, end_date: datetime.datetime
    ) -> set[Room]:
        available_rooms = set(Room.objects.all()) - {
            reservation.room
            for reservation in Reservation.objects.filter(
                start_date__range=(start_date, end_date),
                end_date__range=(start_date, end_date),
            ).select_related('room')
        }
        return available_rooms

    @staticmethod
    def get_default_rooms(today: datetime.datetime) -> set[Room]:
        reservations_today = Reservation.objects.filter(
            start_date__range=(today, today)
        ).select_related('room')
        reserved_desks_today = {reserv.room for reserv in reservations_today}
        all_desks = set(Room.objects.all())
        return all_desks - reserved_desks_today
