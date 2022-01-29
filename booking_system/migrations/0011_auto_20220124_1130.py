# Generated by Django 3.2.9 on 2022-01-24 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking_system', '0010_foodcategory_hotelcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='food_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='booking_system.foodcategory'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='hotel_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='booking_system.hotelcategory'),
        ),
    ]
