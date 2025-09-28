from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

from .views import (
    CreateUserView, 
    CustomTokenObtainPairView, 
    ManageUserView,
    LogoutView,
    AccountsViewSet
)

app_name = 'api-users'

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'', AccountsViewSet)

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', ManageUserView.as_view(), name='me'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]
