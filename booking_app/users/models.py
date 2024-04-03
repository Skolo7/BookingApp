from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Account(AbstractUser):
    username = models.EmailField(unique=True, null=True)
