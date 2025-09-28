from django.contrib.auth import views
from .API.routers import router
from .views import AccountUpdateView, LoginView, RegisterView
from users.views import CustomLogoutView
from django.urls import path
from users.views.password_reset_view import PasswordResetRequestView, PasswordResetConfirmView, PasswordResetDoneCustomView, PasswordResetCompleteCustomView



password_change_patterns = [
    path('password-reset/',
         PasswordResetRequestView.as_view(),
         name='password_reset_request_custom'),
    path('password-reset/done/',
         PasswordResetDoneCustomView.as_view(),
         name='password_reset_done_custom'),
    path('password-reset/<str:token>/',
         PasswordResetConfirmView.as_view(),
         name='password_reset_confirm_custom'),
    path('password-reset/complete/',
         PasswordResetCompleteCustomView.as_view(),
         name='password_reset_complete_custom'),
]


urlpatterns = [
    path('users/register/', RegisterView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', AccountUpdateView.as_view(), name='profile'),
]




urlpatterns += router.urls + password_change_patterns
