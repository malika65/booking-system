# Generated by Django 3.2.9 on 2022-05-18 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking_system', '0026_alter_periodprice_room_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodprice',
            name='room_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='booking_system.room'),
        ),
    ]
