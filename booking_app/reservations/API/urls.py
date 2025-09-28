from django.urls import path
from rest_framework.routers import DefaultRouter
from reservations.API.views import ReservationsViewSet

app_name = 'api-reservations'

router = DefaultRouter()
router.register('', ReservationsViewSet, basename='reservations')

urlpatterns = router.urls