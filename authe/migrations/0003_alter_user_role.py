# Generated by Django 3.2.9 on 2022-01-25 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authe', '0002_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Admin'), (2, 'Managers'), (3, 'Employee'), (4, 'Regular User'), (5, 'Bussiness User')], default=4, null=True),
        ),
    ]