# Generated by Django 3.2.9 on 2022-05-10 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_system', '0013_auto_20220510_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelimage',
            name='image',
            field=models.FileField(upload_to=''),
        ),
    ]
