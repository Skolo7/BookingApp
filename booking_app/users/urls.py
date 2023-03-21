from django.urls import path
from .views import register_view, login_view
from django.contrib.auth import views
from .forms import UserLoginForm

urlpatterns = [
path('register/', register_view, name='register'),
path('login/',  login_view, name='login'),
    #path('login/', views.LoginView.as_view(template_name='users/login.html', authentication_form=UserLoginForm), name='login'),
    ]
