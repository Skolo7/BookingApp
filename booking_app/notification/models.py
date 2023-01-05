from django.db import models
# from booking_app.reservations.models.states import STATUS_TYPES

class Notification(models.Model):
    reservation_id = models.IntegerField
    description = models.TextField(max_length=300)
    # status = models.CharField(max_length=1, choices = STATUS_TYPES)
    type = models.CharField(choices=(('PhoneMessage', 'PhoneMessage'), ('EmailMessage', 'EmailMessage')), max_length=15)

