from django.shortcuts import redirect
from django.shortcuts import render
from reservations.forms import ReservationForm, DateForm, SingleReservationForm, ReserveDeskForm
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


def reserve_desk(request):
    if request.method == 'POST':
        desk_number = request.POST.get('desk_number')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        desk = Desk.objects.get(number=desk_number)
        Reservation.objects.create(desk=desk, start_date=start_date, end_date=end_date,
                                   type=Reservation.ReservationTypes.DESK, person=request.user)

    return redirect(to='reserve')

@login_required
def reserve(request):
    today = timezone.now().date()
    form = ReservationForm(request.POST or None)

    if form.is_valid():
        available_desks = get_filtered_desks(form)
        return render_with_desks(request, available_desks)

    default_desks = get_default_desks(today)
    return render_with_form_and_default_desks(request, form, default_desks, today)


def get_filtered_desks(form):
    start_date = form.cleaned_data['start_date']
    end_date = form.cleaned_data['end_date']
    return get_available_desks(start_date=start_date, end_date=end_date)


def get_default_desks(today):
    reservations_today = Reservation.objects.filter(start_date__range=(today, today)).select_related('desk')
    reserved_desks_today = {reserv.desk for reserv in reservations_today}
    all_desks = set(Desk.objects.all())
    return all_desks - reserved_desks_today


def render_with_desks(request, available_desks):
    context = {'all_desks': available_desks}
    return render(request, 'reserve.html', context=context)


def render_with_form_and_default_desks(request, form, default_desks, today):
    context = {
        'all_desks': default_desks,
        'today': today,
        'form': form,
        'date_form': ReservationForm()
    }
    return render(request, 'reserve.html', context=context)


@login_required
def parking(request):
    if request.method == 'POST':
        form = SingleReservationForm(request.POST)
        if form.is_valid():
            return render(request, 'reserve.html')
    else:
        form = ReservationForm()
    print("Parking View")
    return render(request, 'parking.html')
