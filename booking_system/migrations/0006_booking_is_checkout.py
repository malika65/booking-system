# Generated by Django 3.2.9 on 2022-01-18 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_system', '0005_alter_booking_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='is_checkout',
            field=models.BooleanField(default=False),
        ),
    ]