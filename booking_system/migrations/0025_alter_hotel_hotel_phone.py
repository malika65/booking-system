# Generated by Django 3.2.9 on 2022-02-13 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_system', '0024_auto_20220205_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='hotel_phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Номер телефона отеля'),
        ),
    ]