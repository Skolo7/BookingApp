from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from reservations.views import index

urlpatterns = [
                  path('', include('reservations.urls')),
                  path('', index, name='index'),
                  path("users/", include("users.urls")),
                  path("^", include("django.contrib.auth.urls")),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

