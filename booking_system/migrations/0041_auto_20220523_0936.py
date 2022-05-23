# Generated by Django 3.2.9 on 2022-05-23 09:36

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('booking_system', '0040_auto_20220523_0825'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='room',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='hotel', chained_model_field='hotel_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='booking_system.room', verbose_name='Номер'),
        ),
        migrations.AlterField(
            model_name='room',
            name='hotel_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='room', to='booking_system.hotel', verbose_name='Отель'),
        ),
    ]