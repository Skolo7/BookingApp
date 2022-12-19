from django.db import models
from django.contrib.postgres.fields import ArrayField

class Person(models.Model):
    name = models.CharField(max_length=15)
    surname = models.CharField(max_length=30)
    mail = models.EmailField(max_length=30)
    password = models.CharField(max_length=50)
    login = models.CharField(max_length=25)
    VIP = models.BooleanField(default=False)
    user_reservations = ArrayField

