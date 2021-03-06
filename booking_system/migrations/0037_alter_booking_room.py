# Generated by Django 3.2.9 on 2022-05-23 08:07

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('booking_system', '0036_alter_booking_hotel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='room',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='hotel', chained_model_field='hotel', null=True, on_delete=django.db.models.deletion.CASCADE, to='booking_system.room', verbose_name='Номер'),
        ),
    ]
