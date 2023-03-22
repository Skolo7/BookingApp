from django.db import models
from .reservations import Reservation
from .states import ProductState


class Parking(models.Model):
    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.CASCADE,
        related_name='parking'
    )
    number = models.IntegerField()
    floor = models.IntegerField()
    status = models.CharField(max_length=10, choices=ProductState.choices, default=ProductState.AVAILABLE)


class Room(models.Model):
    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.CASCADE,
        related_name='room'
    )
    name = models.CharField(max_length=20)
    number = models.PositiveIntegerField()
    max_amount_of_people = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=ProductState.choices, default=ProductState.AVAILABLE)


class Desk(models.Model):
    class DeskTypes(models.TextChoices):
        SMALL_DESK = "small_desk", "small_desk"
        NARROW_DESK = "narrow_desk", "narrow_desk"
        MEDIUM_DESK = "medium_desk", "medium_desk"
        LARGE_DESK = "large_desk", "large_desk"

    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.CASCADE,
        related_name='desk'
    )
    name = models.CharField(max_length=20)
    number = models.PositiveIntegerField()
    status = models.CharField(max_length=15, choices=ProductState.choices, default=ProductState.AVAILABLE)
    type = models.CharField(max_length=15, choices=DeskTypes.choices)