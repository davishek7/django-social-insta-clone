# Generated by Django 3.2 on 2023-05-14 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0006_alter_notification_entity_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='entity_id',
            field=models.BigIntegerField(blank=True, default=None, null=True),
        ),
    ]
