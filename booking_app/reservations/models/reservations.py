from django.conf import settings
from django.db import models
from .products import Desk, Room, Parking


class Reservation(models.Model):
    class ReservationTypes(models.TextChoices):
        DESK = "DESK", "DESK"
        ROOM = "ROOM", "ROOM"
        PARKING = "PARKING", "PARKING"

    start_date = models.DateField(help_text="date when reservations began")
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now=True)
    desk = models.ForeignKey(
        Desk,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='reservations',
    )
    room = models.ForeignKey(
        Room,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='reservations',
    )
    parking = models.ForeignKey(
        Parking,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='reservations',
    )
    title = models.CharField(
        null=True,
        blank=True,
        max_length=50,
    )
    description = models.CharField(
        null=True,
        blank=True,
        max_length=255,
    )
    person = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE, blank=True, null=True, related_name='reservations')
    type = models.CharField(max_length=35, choices=ReservationTypes.choices)

    def __str__(self) -> str:
        return str(self.title)
