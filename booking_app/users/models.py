from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        default='profile_pics/Profile_pic.png',
    )

    def __str__(self) -> str:
        return self.username if self.username else "Unnamed Account"
