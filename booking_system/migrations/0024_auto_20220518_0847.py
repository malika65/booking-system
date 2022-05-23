# Generated by Django 3.2.9 on 2022-05-18 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking_system', '0023_auto_20220518_0845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='price',
        ),
        migrations.AddField(
            model_name='periodprice',
            name='room_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='booking_system.room', verbose_name='Комната'),
        ),
    ]