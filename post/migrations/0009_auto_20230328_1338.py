# Generated by Django 3.2 on 2023-03-28 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_auto_20230328_1333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='replies',
        ),
        migrations.AddField(
            model_name='reply',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_replies', to='post.comment'),
        ),
    ]