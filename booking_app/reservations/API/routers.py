from rest_framework.routers import DefaultRouter

from .views import ReservationsViewSet

router = DefaultRouter()
router.include_root_view = False

router.register(r"api/v1/reservations", ReservationsViewSet)
