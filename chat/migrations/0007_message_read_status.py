# Generated by Django 3.2 on 2023-06-05 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_alter_inbox_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='read_status',
            field=models.BooleanField(default=False),
        ),
    ]