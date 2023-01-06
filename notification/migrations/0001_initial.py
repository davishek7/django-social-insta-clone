# Generated by Django 3.2 on 2023-01-04 03:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0005_auto_20220922_0901'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('from_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_sender', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='notification_post', to='post.post')),
                ('to_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_receiver', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
