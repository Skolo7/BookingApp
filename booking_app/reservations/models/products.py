from django.db import models

from .states import ProductState


class Parking(models.Model):
    number = models.PositiveIntegerField()
    status = models.CharField(
        max_length=10, choices=ProductState.choices, default=ProductState.AVAILABLE
    )
    #
    #
    # def __str__(self):
    #     return str(self.number) or ''


class Room(models.Model):
    class RoomTypes(models.TextChoices):
        RED_ROOM = "red_room", "red_room"
        YELLOW_ROOM = "yellow_room", "yellow_room"
        GREEN_ROOM = "green_room", "green_room"
        BLUE_ROOM = "blue_room", "blue_room"

    name = models.CharField(max_length=20)
    number = models.PositiveIntegerField()
    max_amount_of_people = models.PositiveIntegerField()
    status = models.CharField(
        max_length=10, choices=ProductState.choices, default=ProductState.AVAILABLE
    )
    type = models.CharField(max_length=15, choices=RoomTypes.choices)

    def __str__(self):
        return str(self.type)


class Desk(models.Model):
    class DeskTypes(models.TextChoices):
        SMALL_DESK = "small_desk", "small_desk"
        NARROW_DESK = "narrow_desk", "narrow_desk"
        MEDIUM_DESK = "medium_desk", "medium_desk"
        LARGE_DESK = "large_desk", "large_desk"

    name = models.CharField(max_length=20)
    number = models.PositiveIntegerField()
    status = models.CharField(
        max_length=15, choices=ProductState.choices, default=ProductState.AVAILABLE
    )
    type = models.CharField(max_length=15, choices=DeskTypes.choices)

    # def __str__(self):
    #     return str(self.number)
