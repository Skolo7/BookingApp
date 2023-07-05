# Generated by Django 4.1.4 on 2023-03-22 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.TextField(max_length=300)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("PhoneMessage", "PhoneMessage"),
                            ("EmailMessage", "EmailMessage"),
                        ],
                        max_length=15,
                    ),
                ),
            ],
        ),
    ]
