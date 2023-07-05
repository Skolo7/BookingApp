from django.db import models

class ProductState(models.TextChoices):
    AVAILABLE = "AVAILABLE", "AVAILABLE"
    RESERVED = "RESERVED", "RESERVED"
