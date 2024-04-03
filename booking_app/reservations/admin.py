from django.contrib import admin

from .models import Desk, Parking, Reservation, Room


@admin.register(Reservation)
class AdminReservation(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'desk', 'room', 'parking')


@admin.register(Desk)
class AdminDesk(admin.ModelAdmin):
    list_display = ('id', 'number', 'status', 'type')
    list_filter = ('status', 'type')
    ordering = (
        'id',
        'number',
    )


@admin.register(Parking)
class AdminParking(admin.ModelAdmin):
    list_display = ('number', 'status')


@admin.register(Room)
class AdminRoom(admin.ModelAdmin):
    list_display = ('number', 'max_amount_of_people', 'status', 'type')
