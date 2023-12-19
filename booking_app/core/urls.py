from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from reservations.views import IndexView
from django.contrib.auth import views
from django.contrib.auth import urls

urlpatterns = [
                  path('', include('reservations.urls')),
                  path('', IndexView.as_view(), name='index'),
                  path("users/", include("users.urls")),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + password_change_patterns
