# Generated by Django 3.2 on 2023-01-10 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_auto_20220922_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]
