from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from reservations.views import CustomDashboardView, IndexView

api_patterns = [
    path('users/', include('users.API.urls', namespace='api-users')),
    path('reservations/', include('reservations.API.urls', namespace='api-reservations')),
    path('auth/', include([
        path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ])),
]
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('dashboard/', CustomDashboardView.as_view(), name='dashboard'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('reservations/', include('reservations.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include(api_patterns)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)