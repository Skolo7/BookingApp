from django.shortcuts import redirect
from django.shortcuts import render
from reservations.forms import ReservationForm, DateForm
from reservations.models import Desk, Reservation
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import logging


logger = logging.getLogger(__name__)


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def reserve(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            available_desks = set(Desk.objects.all()) - {reserv.desk for reserv in
                                                         Reservation.objects.filter(
                                                             start_date__range=(start_date, end_date),
                                                             end_date__range=(start_date, end_date)).select_related(
                                                             'desk')}
            context = {'all_desks': available_desks}
            context['form'] = ReservationForm()
            return render(request, 'reserve.html', context=context)
            # return redirect('office')
    else:
        form = ReservationForm()
    print("Office Vie")

    # start_date, end_date = timezone.now().date(), timezone.now().date()
    #TODO maybe refactor in the future.
    today = timezone.now().date()
    available_desks = set(Desk.objects.all()) - {reserv.desk for reserv in
                                                 Reservation.objects.filter(
                                                     start_date__range=(today, today),
                                                     end_date__range=(today, today)).select_related(
                                                     'desk')}
    context = {'all_desks': available_desks, 'today': today}
    context['form'] = ReservationForm()
    context['date_form'] = DateForm()
    return render(request, 'reserve.html', context=context)


# Reservation.objects.filter(start_date__range=(start_date, end_date), end_date__range=(start_date, end_date)).select_related('desk')[0].desk
# Reservation.objects.filter(start_date__range=(start_date, end_date), end_date__range=(start_date, end_date)).select_related('desk')[0].desk
# {reserv.desk for reserv in Reservation.objects.filter(start_date__range=(start_date, end_date),
#                                                       end_date__range=(start_date, end_date)).select_related(
#     'desk')}
# available_desks = set(Desk.objects.all()) - {reserv.desk for reserv in
#                            Reservation.objects.filter(start_date__range=(start_date, end_date),
#                                                       end_date__range=(start_date, end_date)).select_related(
#                                'desk')}
# reservation = Reservation.objects.filter(start_date__range=(start_date, end_date), end_date__range=(start_date, end_date))
# print(reservation)
# x = Reservation.objects.all()
# desks = Desk.objects.all()

# context = {'all_desks': available_desks}