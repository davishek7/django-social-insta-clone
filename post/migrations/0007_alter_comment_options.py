# Generated by Django 3.2 on 2023-02-11 04:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_alter_comment_body'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_at']},
        ),
    ]
