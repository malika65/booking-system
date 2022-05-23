# Generated by Django 3.2.9 on 2022-05-23 07:28

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('booking_system', '0028_alter_hotel_room_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='room',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='hotel', chained_model_field='hotel', on_delete=django.db.models.deletion.CASCADE, to='booking_system.room', verbose_name='Комната'),
        ),
    ]