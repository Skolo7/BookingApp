from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import urls, views
from django.urls import include, path
from reservations.views import IndexView

password_change_patterns = [
    path(
        "password_change/", views.PasswordChangeView.as_view(), name="password_change"
    ),
    path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
urlpatterns = (
    [
        path('', include('reservations.urls')),
        path('', IndexView.as_view(), name='index'),
        path('', include("users.urls")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + password_change_patterns
)
