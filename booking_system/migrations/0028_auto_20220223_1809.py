# Generated by Django 3.2.9 on 2022-02-23 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_system', '0027_remove_characteristics_hotel_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='characteristics',
            name='room_id',
        ),
        migrations.AddField(
            model_name='characteristics',
            name='room_id',
            field=models.ManyToManyField(blank=True, null=True, to='booking_system.Room', verbose_name='Комната'),
        ),
        migrations.RemoveField(
            model_name='room',
            name='hotel_id',
        ),
        migrations.AddField(
            model_name='room',
            name='hotel_id',
            field=models.ManyToManyField(blank=True, null=True, to='booking_system.Hotel', verbose_name='Отель'),
        ),
    ]