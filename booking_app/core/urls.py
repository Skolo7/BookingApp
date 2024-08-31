from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from reservations.views import IndexView

urlpatterns = (
    [
        path('', include('reservations.urls')),
        path('', IndexView.as_view(), name='index'),
        path('', include("users.urls")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
