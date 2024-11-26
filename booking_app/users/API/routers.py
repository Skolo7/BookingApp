from rest_framework.routers import DefaultRouter

from .views import AccountsViewSet

router = DefaultRouter()
router.include_root_view = False

router.register(r'api/v1/accounts', AccountsViewSet)
