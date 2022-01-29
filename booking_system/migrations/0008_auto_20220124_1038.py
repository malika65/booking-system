# Generated by Django 3.2.9 on 2022-01-24 04:38

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('booking_system', '0007_auto_20220119_1058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='country_id',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='city_id',
        ),
        migrations.AddField(
            model_name='hotel',
            name='city',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='country', chained_model_field='country_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='booking_system.city'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='booking_system.country'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='category_id',
            field=models.ManyToManyField(blank=True, default='Hotel', null=True, to='booking_system.Category'),
        ),
    ]