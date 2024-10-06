from rest_framework.routers import DefaultRouter
from .views import ReservationsViewSet

router = DefaultRouter()
router.register(r'reservations', ReservationsViewSet)