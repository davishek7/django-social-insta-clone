# Generated by Django 3.2 on 2022-09-15 02:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='status',
            new_name='is_active',
        ),
    ]
