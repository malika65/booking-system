# Generated by Django 3.2.9 on 2022-06-13 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking_system', '0048_auto_20220613_0641'),
    ]

    operations = [
        migrations.AddField(
            model_name='facilitiesandserviceshotels',
            name='category_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='booking_system.category', verbose_name='Подкатегория'),
        ),
    ]
