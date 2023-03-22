from django.shortcuts import redirect
from django.shortcuts import render
from reservations.forms import ReservationForm


def index(request):
    return render(request, 'index.html')


def office(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            return redirect('office')
    else:
        form = ReservationForm()
    context = {}
    context['form'] = ReservationForm()
    return render(request, 'office.html', context=context)