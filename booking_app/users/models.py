from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    username = models.EmailField(unique=True, null=True)




