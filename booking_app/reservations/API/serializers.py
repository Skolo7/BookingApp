from rest_framework import serializers
from reservations.models.reservations import Reservation


class ReservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            "id",
            "start_date",
            "end_date",
            "created_at",
            "desk",
            "room",
            "parking",
            "title",
            "description",
            "person",
            "type",
        ]
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        if 'start_date' in data and 'end_date' in data:
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError(
                    {"end_date": "end date cannot be before start date."}
                )
        return data