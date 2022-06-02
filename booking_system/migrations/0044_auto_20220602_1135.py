# Generated by Django 3.2.9 on 2022-06-02 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_system', '0043_auto_20220525_1124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='room',
        ),
        migrations.AddField(
            model_name='booking',
            name='room',
            field=models.ManyToManyField(blank=True, null=True, to='booking_system.Room', verbose_name='Номер'),
        ),
    ]
