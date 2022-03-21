# Generated by Django 3.2.9 on 2022-02-13 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authe', '0006_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[(1, 'Admin'), (2, 'Managers'), (3, 'Employee'), (4, 'Regular User'), (5, 'Bussiness User'), (6, 'Tour Operator')], default=4, max_length=20, null=True),
        ),
    ]