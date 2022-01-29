# Generated by Django 3.2.9 on 2022-01-24 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_system', '0009_city_country_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foodcategory_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='HotelCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotelcategory_name', models.CharField(max_length=50)),
            ],
        ),
    ]
