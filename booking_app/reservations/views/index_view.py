from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


# To nie powinno chyba tutaj być? Jakaś apka dashboard? 
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
