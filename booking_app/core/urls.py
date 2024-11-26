from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from reservations.views import IndexView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = (
    [
        path('', include('reservations.urls')),
        path('', IndexView.as_view(), name='index'),
        path('', include("users.urls")),
        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
