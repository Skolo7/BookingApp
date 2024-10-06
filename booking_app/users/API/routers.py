from rest_framework.routers import DefaultRouter
from .views import AccountsViewSet

router = DefaultRouter()
router.register(r'api/accounts', AccountsViewSet)