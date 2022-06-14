# Generated by Django 3.2.9 on 2022-06-14 08:48

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_system', '0054_alter_hotelimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelimage',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='images'),
        ),
    ]