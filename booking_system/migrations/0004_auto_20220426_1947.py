# Generated by Django 3.2.9 on 2022-04-26 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking_system', '0003_auto_20220426_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='additionalservice',
            name='name_en',
            field=models.CharField(max_length=50, null=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='additionalservice',
            name='name_ru',
            field=models.CharField(max_length=50, null=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='childservice',
            name='name_en',
            field=models.CharField(max_length=50, null=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='childservice',
            name='name_ru',
            field=models.CharField(max_length=50, null=True, verbose_name='Название'),
        ),
    ]
