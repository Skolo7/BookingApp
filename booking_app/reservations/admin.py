from django.contrib import admin

from .models import Reservation, Parking, Desk, Room

@admin.register(Reservation)
class AdminReservation(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'desk', 'room', 'parking')


@admin.register(Desk)
class AdminDesk(admin.ModelAdmin):
    list_display = ('number', )

@admin.register(Parking)
class AdminParking(admin.ModelAdmin):
    list_display = ('number', )

@admin.register(Room)
class AdminRoom(admin.ModelAdmin):
    list_display = ('number', )
