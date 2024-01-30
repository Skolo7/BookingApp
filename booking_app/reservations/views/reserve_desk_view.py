from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from ..models.products import Desk
from ..models.reservations import Reservation
from ..forms import FilterAvailabilityForm, ReserveDeskForm
from django.contrib.auth.mixins import LoginRequiredMixin


class FilterDeskView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = FilterAvailabilityForm(request.POST)
        print(form)
        print(form.is_valid())
        start_date, end_date = form.cleaned_data['start_date'], form.cleaned_data['end_date']
        request.session['start_date'] = start_date.strftime("%Y-%m-%d")
        request.session['end_date'] = end_date.strftime("%Y-%m-%d")
        return redirect('reserve')


class ReserveDeskView(LoginRequiredMixin, View):
    template_name = 'reserve.html'

    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        reservation_form = ReserveDeskForm()

        start_date_str = request.session.get('start_date')
        end_date_str = request.session.get('end_date')

        if start_date_str and end_date_str:
            start_date = timezone.datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = timezone.datetime.strptime(end_date_str, "%Y-%m-%d").date()
            available_desks = self.get_available_desks(start_date, end_date)
        else:
            available_desks = self.get_default_desks(today)
        return self.render_with_form_and_desks(request, available_desks, today, reservation_form)

    def post(self, request, *args, **kwargs):
        form = ReserveDeskForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.person = self.request.user
            desk_number = form.data['desk_number']
            reservation.desk = Desk.objects.get(number=desk_number)
            reservation.save()
            self.get(request)
        else:
            print(form.errors)
        return self.get(request)

    @staticmethod
    def get_default_desks(today):
        reservations_today = Reservation.objects.filter(start_date__range=(today, today)).select_related('desk')
        reserved_desks_today = {reserv.desk for reserv in reservations_today}
        all_desks = set(Desk.objects.all())
        return all_desks - reserved_desks_today

    def render_with_form_and_desks(self, request, desks, today, reservation_form):
        context = {
            'all_desks': desks,
            'today': today,
            'filter_form': FilterAvailabilityForm(),
            'reservation_form': reservation_form
        }
        return render(request, self.template_name, context=context)

    def get_filtered_desks(self, form):
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        return self.get_available_desks(start_date=start_date, end_date=end_date)

    def get_available_desks(self, start_date, end_date):
        available_desks = set(Desk.objects.all()) - {reserv.desk for reserv in
                                                     Reservation.objects.filter(
                                                         start_date__range=(start_date, end_date),
                                                         end_date__range=(start_date, end_date)).select_related(
                                                         'desk')}
        return available_desks
