# Generated by Django 3.2 on 2023-06-07 04:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_user_website'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoggedUser',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='account.user')),
            ],
        ),
    ]
