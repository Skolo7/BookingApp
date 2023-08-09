from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager


class Account(AbstractUser, PermissionsMixin):
    username = models.EmailField(unique=True, null=True)
    first_name = models.CharField(max_length=30, help_text="")
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []



