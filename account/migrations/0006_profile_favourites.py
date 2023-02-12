# Generated by Django 3.2 on 2023-02-11 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_alter_comment_options'),
        ('account', '0005_alter_user_profile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='favourites',
            field=models.ManyToManyField(blank=True, related_name='user_favourites', to='post.Post'),
        ),
    ]