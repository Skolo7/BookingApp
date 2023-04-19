# Generated by Django 4.1.4 on 2023-03-23 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("reservations", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="desk",
            name="reservation",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reservations",
                to="reservations.reservation",
            ),
        ),
    ]
