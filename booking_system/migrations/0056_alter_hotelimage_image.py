# Generated by Django 3.2.9 on 2022-06-14 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_system', '0055_alter_hotelimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelimage',
            name='image',
            field=models.ImageField(upload_to='', verbose_name='images'),
        ),
    ]
