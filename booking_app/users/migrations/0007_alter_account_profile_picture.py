# Generated by Django 5.0.4 on 2024-06-15 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_account_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_pics/Profile_pic.png', null=True, upload_to='profile_pics/'),
        ),
    ]