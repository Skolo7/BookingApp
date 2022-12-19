from django.db import models
from django.conf import settings
from static import STATUS_TYPES


class Reservation(models.Model):
    start_date = models.DateTimeField(help_text="date when reservation began")
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now=True)
    title = models.CharField(
        null=True,
        blank=True,
    )
    description = models.CharField(
        null=True,
        blank=True,
    )
    person = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE, blank = True, null = True)
    #TODO Type



class Parking(models.Model):
    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.CASCADE,
        related_name='parking'
    )
    number = models.IntegerField(max_length=10)
    floor = models.IntegerField(max_length=1)
    status = models.CharField(max_length=1, choices=STATUS_TYPES)


class Room(models.Model):
    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.CASCADE,
        related_name='room'
    )
    name = models.CharField(max_length=20)
    number = models.IntegerField(max_length=2)
    max_amount_of_people = models.IntegerField
    status = models.CharField(max_length=1, choices=STATUS_TYPES)


class Desk(models.Model):
    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.CASCADE,
        related_name='desk'
    )
    name = models.CharField(max_length=20)
    number = models.IntegerField(max_length=2)
    status = models.CharField(max_length=1, choices=STATUS_TYPES)