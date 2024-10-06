from rest_framework import viewsets
from ..models import Reservation
from .serializers import ReservationsSerializer


class ReservationsViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationsSerializer