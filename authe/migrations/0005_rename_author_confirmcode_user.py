# Generated by Django 3.2.9 on 2022-02-03 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authe', '0004_confirmcode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='confirmcode',
            old_name='author',
            new_name='user',
        ),
    ]