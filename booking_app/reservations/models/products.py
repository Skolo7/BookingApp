from django.db import models

from .states import ProductState


class Parking(models.Model):
    number = models.PositiveIntegerField(help_text="Unique parking spot number")
    status = models.CharField(
        max_length=10, choices=ProductState.choices, default=ProductState.AVAILABLE, 
        help_text="Current status of the parking spot"
    )




class Room(models.Model):
    class RoomTypes(models.TextChoices):
        RED_ROOM = "red_room", "red_room"
        YELLOW_ROOM = "yellow_room", "yellow_room"
        GREEN_ROOM = "green_room", "green_room"
        BLUE_ROOM = "blue_room", "blue_room"

    name = models.CharField(
        max_length=20,
        help_text="Name identifier for the room"
    )
    number = models.PositiveIntegerField(
        help_text="Unique room number"
    )
    max_amount_of_people = models.PositiveIntegerField(
        help_text="Maximum number of people allowed in the room"
    )
    status = models.CharField(
        max_length=10, 
        choices=ProductState.choices, 
        default=ProductState.AVAILABLE,
        help_text="Current status of the room"
    )
    type = models.CharField(
        max_length=15, 
        choices=RoomTypes.choices,
        help_text="Type/color designation of the room"
    )

    def __str__(self) -> str:
        return f"{str(self.type)}"


class Desk(models.Model):
    class DeskTypes(models.TextChoices):
        SMALL_DESK = "small_desk", "small_desk"
        NARROW_DESK = "narrow_desk", "narrow_desk"
        MEDIUM_DESK = "medium_desk", "medium_desk"
        LARGE_DESK = "large_desk", "large_desk"

    name = models.CharField(
        max_length=20,
        help_text="Name identifier for the desk"
    )
    number = models.PositiveIntegerField(
        help_text="Unique desk number"
    )
    status = models.CharField(
        max_length=15, 
        choices=ProductState.choices, 
        default=ProductState.AVAILABLE,
        help_text="Current status of the desk"
    )
    type = models.CharField(
        max_length=15, 
        choices=DeskTypes.choices,
        help_text="Size/type designation of the desk"
    )