# Generated by Django 3.2.9 on 2022-05-05 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_system', '0005_alter_childservice_until_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelimage',
            name='images',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
