from django.apps import AppConfig


class ReservationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservations'

    # def ready(self):
    #     from .script import setup_desks
    #     post_migrate.connect(setup_desks, sender=self)