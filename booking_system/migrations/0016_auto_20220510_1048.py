# Generated by Django 3.2.9 on 2022-05-10 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_system', '0015_periodprice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='price',
        ),
        migrations.AddField(
            model_name='room',
            name='price',
            field=models.ManyToManyField(to='booking_system.PeriodPrice'),
        ),
    ]
