from django.shortcuts import redirect
from django.shortcuts import render
from reservations.forms import ReservationForm


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def reserve(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            return redirect('office')
    else:
        form = ReservationForm()
    context = {}
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