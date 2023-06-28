from django.shortcuts import redirect
from django.shortcuts import render
from reservations.forms import ReservationForm, DateForm, SingleReservationForm
from reservations.models import Desk, Reservation
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import logging
from django.shortcuts import render
from users.models import Account


def reservations(request):
    reservations = Account.objects.all()
    return render(request, '../reservations_template.html')


logger = logging.getLogger(__name__)


@login_required
def index(request):
    return render(request, 'index.html')


def get_available_desks(start_date, end_date):
    available_desks = set(Desk.objects.all()) - {reserv.desk for reserv in
                                                 Reservation.objects.filter(
                                                     start_date__range=(start_date, end_date),
                                                     end_date__range=(start_date, end_date)).select_related(
                                                     'desk')}
    return available_desks


@login_required
def reserve(request):
    if request.method == 'POST':
        if request.POST['form_type'] == 'reserve':
            form = ReservationForm()
            if form.is_valid():
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                available_desks = get_available_desks(start_date=start_date, end_date=start_date)

            context = {'all_desks': available_desks}
        else:
            form = SingleReservationForm(request.POST)
            if form.is_valid():
                # TODO ZAKRES DAT.



                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['start_date']
                available_desks = get_available_desks(start_date=start_date, end_date=end_date)






                context = {'all_desks': available_desks}
                context['date_form'] = SingleReservationForm()
                # context['form'] = ReservationForm()
            return render(request, 'reserve.html', context=context)
    else:
        form = ReservationForm()

    # start_date, end_date = timezone.now().date(), timezone.now().date()
    # TODO refactor in the future.
    today = timezone.now().date()
    available_desks = set(Desk.objects.all()) - {reserv.desk for reserv in
                                                 Reservation.objects.filter(
                                                     start_date__range=(today, today)).select_related(
                                                     'desk')}
    form = ReservationForm()
    context = {'all_desks': available_desks, 'today': today, 'form': form}
    context['date_form'] = SingleReservationForm()
    return render(request, 'reserve.html', context=context)

@login_required
def parking(request):
    if request.method == 'POST':
        form = SingleReservationForm(request.POST)
        if form.is_valid():
            # start_date = form.cleaned_data['start_date']
            # end_date = form.cleaned_data['start_date']
            # available_desks = set(Desk.objects.all()) - {reserv.parking for reserv in
            #                                              Reservation.objects.filter(
            #                                                  start_date__range=(start_date, end_date),
            #                                                  end_date__range=(start_date, end_date)).select_related(
            #                                                  'desk')}
            # context = {'all_desks': available_desks}
            # context['date_form'] = SingleReservationForm()
            # # context['form'] = ReservationForm()
            return render(request, 'reserve.html')
    else:
        form = ReservationForm()
    print("Parking View")
    #
    # today = timezone.now().date()
    # available_desks = set(Desk.objects.all()) - {reserv.desk for reserv in
    #                                              Reservation.objects.filter(
    #                                                  start_date__range=(today, today),
    #                                                  end_date__range=(today, today)).select_related(
    #                                                  'desk')}
    # context = {'all_desks': available_desks, 'today': today}
    # context['form'] = ReservationForm()
    # context['date_form'] = SingleReservationForm()
    return render(request, 'parking.html')
