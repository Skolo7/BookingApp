from django.contrib.auth import logout
from django.shortcuts import render
from django.views import View


class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'users/logout_template.html')

    def post(self, request):
        logout(request)
        return render(request, 'users/logout_template.html')