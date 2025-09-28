from django.contrib.auth.models import AbstractUser
from django.db import models
import logging

logger = logging.getLogger(__name__)


class Account(AbstractUser):
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        default='profile_pics/Profile_pic.png',
    )
    email = models.EmailField("email address", blank=True, unique=True)

    def __str__(self) -> str:
        return self.username if self.username else "Unnamed Account"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            logger.info(f"New account created: {self.username}")
        else:
            logger.debug(f"Account updated: {self.username}")
