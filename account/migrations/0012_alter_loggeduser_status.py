# Generated by Django 3.2 on 2023-07-22 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20230607_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loggeduser',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]