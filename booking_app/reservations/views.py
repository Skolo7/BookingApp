from django.shortcuts import redirect
from django.shortcuts import render
# from reservations.forms import ReservationForm, DateForm, SingleReservationForm
from models import Desk, Reservation
from users/models import Account
# from django.utils import timezone
# from django.contrib.auth.decorators import login_required
# import logging

def reservations(request):
    reservations = Account.objects.all()
    return render(request, '../reservations_template.html')