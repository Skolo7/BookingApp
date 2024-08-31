from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from icecream import ic

from ..forms import FilterAvailabilityForm, ReserveForm
from ..models.products import Desk, Room
from ..models.reservations import Reservation


class FilterDeskView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = FilterAvailabilityForm(request.POST)
        print(form)
        print(form.is_valid())
        start_date, end_date = (
            form.cleaned_data['start_date'],
            form.cleaned_data['end_date'],
        )
        start_date_param = start_date.strftime("%Y-%m-%d")
        end_date_param = end_date.strftime("%Y-%m-%d")
        return redirect(
            f'/reserve?start_date={start_date_param}&end_date={end_date_param}'
        )


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
                messages.error(request, 'Cant reserve for past days.')
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
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.person = self.request.user
            number, type = form.data['number'], form.data['type']
            today = timezone.now().date()

            if reservation.start_date < today or reservation.end_date < today:
                messages.error(request, 'Cant reserve for past days!')
                return self.get(request)

            if type == 'room':
                reservation.room = Room.objects.get(number=number)
                reservation.type = 'ROOM'
            elif type == 'desk':
                reservation.desk = Desk.objects.get(number=number)
                reservation.type = 'DESK'

            reservation.save()
            messages.success(request, 'Reservation confirmed.')
        else:
            messages.error(request, 'Reservation failure.')
        return self.get(request)

    @staticmethod
    def get_default_desks(today):  # TODO Typing
        reservations_today = Reservation.objects.filter(
            start_date__range=(today, today)
        ).select_related('desk')
        reserved_desks_today = {reserv.desk for reserv in reservations_today}
        all_desks = set(Desk.objects.all())
        return all_desks - reserved_desks_today

    def render_with_form_and_desks(
        self, request, desks, rooms, today, reservation_form
    ): # TODO Typing
        context = {
            'all_desks': desks,
            'all_rooms': rooms,
            'today': today,
            'filter_form': FilterAvailabilityForm(),
            'reservation_form': reservation_form,
        }
        return render(request, self.template_name, context=context)

    def get_filtered_desks(self, form):  # TODO Typing
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        return self.get_available_desks(start_date=start_date, end_date=end_date)

    def get_available_desks(self, start_date, end_date): # TODO Typing
        available_desks = set(Desk.objects.all()) - { # TODO literally
            reserv.desk
            for reserv in Reservation.objects.filter( # TODO literally
                start_date__range=(start_date, end_date),
                end_date__range=(start_date, end_date),
            ).select_related('desk')
        }
        return available_desks

    def get_available_rooms(self, start_date, end_date):
        avaialble_rooms = set(Room.objects.all()) - { # TODO literally
            reserv.room
            for reserv in Reservation.objects.filter( # TODO literally
                start_date__range=(start_date, end_date),
                end_date__range=(start_date, end_date),
            ).select_related('room')
        }
        return avaialble_rooms

    @staticmethod
    def get_default_rooms(today):
        reservations_today = Reservation.objects.filter(
            start_date__range=(today, today)
        ).select_related('room')
        reserved_desks_today = {reserv.room for reserv in reservations_today}
        all_desks = set(Room.objects.all())
        return all_desks - reserved_desks_today
