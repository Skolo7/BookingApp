from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30, unique=True)
    password = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    user_reservations = ArrayField
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']


# class Person(models.Model):
#     name = models.CharField(max_length=15)
#     surname = models.CharField(max_length=30)
#     mail = models.EmailField(max_length=30)
#     password = models.CharField(max_length=50)
#     login = models.CharField(max_length=25)
#     VIP = models.BooleanField(default=False)
#     user_reservations = ArrayField

