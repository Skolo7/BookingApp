from django.urls import path, include
from .views import RegisterView, LoginView
from django.contrib.auth import views
from .forms import UserLoginForm

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # path('logout_redirect_to_login/', logout_view, name='logout_redirect_to_login'),
]
