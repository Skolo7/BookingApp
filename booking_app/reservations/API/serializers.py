from rest_framework import serializers
from reservations.models import Reservation


class ReservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['start_date', 'end_date', 'created_at', 'desk', 'room', 'parking', 'title', 'description', 'person',
                  'type']
