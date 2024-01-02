# Generated by Django 4.1.4 on 2023-12-27 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reservations", "0010_alter_reservation_person_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("red_room", "red_room"),
                    ("yellow_room", "yellow_room"),
                    ("green_room", "green_room"),
                    ("blue_room", "blue_room"),
                ],
                default=None,
                max_length=15,
                null=True,
            ),
        ),
    ]
