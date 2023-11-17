from django.urls import path, include
from .views import register_view, login_view, logout_view
from django.contrib.auth import views
from .forms import UserLoginForm

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout_redirect_to_login/', logout_view, name='logout_redirect_to_login'),
]
