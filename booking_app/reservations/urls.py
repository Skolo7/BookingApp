from django.contrib import admin
from django.urls import path
from .API.routers import router

from .views import (
    FilterDeskView,
    FilterParkingView,
    ReservationListView,
    ReserveDeskView,
    ReserveParkingView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user-reservations/', ReservationListView.as_view(), name='user-reservations'),
    path('reserve/', ReserveDeskView.as_view(), name='reserve'),
    path('parking/', ReserveParkingView.as_view(), name='parking'),
    path('filter-desks', FilterDeskView.as_view(), name='filter-desk-view'),
    path('filter-parkings', FilterParkingView.as_view(), name='filter-parking-view'),
]

urlpatterns += router.urls
