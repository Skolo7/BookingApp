from django.conf import settings
from django.db import models

from .products import Desk, Parking, Room


class Reservation(models.Model):
    class ReservationTypes(models.TextChoices):
        DESK = "DESK", "DESK"
        ROOM = "ROOM", "ROOM"
        PARKING = "PARKING", "PARKING"

    start_date = models.DateField(
        help_text="Start date of the reservation"
    )
    end_date = models.DateField(
        help_text="End date of the reservation"
    )
    created_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the reservation was created"
    )
    desk = models.ForeignKey(
        Desk,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='reservations',
        help_text="Associated desk for the reservation (if desk type)"
    )
    room = models.ForeignKey(
        Room,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='reservations',
        help_text="Associated room for the reservation (if room type)"
    )
    parking = models.ForeignKey(
        Parking,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='reservations',
        help_text="Associated parking spot for the reservation (if parking type)"
    )
    title = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        help_text="Optional title for the reservation"
    )
    description = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text="Optional description for the reservation"
    )
    person = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='reservations',
        help_text="User who made the reservation"
    )
    type = models.CharField(
        max_length=35, 
        choices=ReservationTypes.choices,
        help_text="Type of reservation (desk, room, or parking)"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['desk', 'start_date', 'end_date'],
                name='unique_desk_reservation_per_period',
                condition=models.Q(desk__isnull=False)
            ),
            models.UniqueConstraint(
                fields=['room', 'start_date', 'end_date'],
                name='unique_room_reservation_per_period',
                condition=models.Q(room__isnull=False)
            ),
            models.UniqueConstraint(
                fields=['parking', 'start_date', 'end_date'],
                name='unique_parking_reservation_per_period',
                condition=models.Q(parking__isnull=False)
            ),
        ]