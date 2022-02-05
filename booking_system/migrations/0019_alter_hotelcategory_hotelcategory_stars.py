# Generated by Django 3.2.9 on 2022-02-05 13:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_system', '0018_alter_hotelcategory_hotelcategory_stars'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelcategory',
            name='hotelcategory_stars',
            field=models.IntegerField(blank=True, default=5, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)]),
        ),
    ]
