# Generated by Django 5.1.2 on 2024-10-21 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoApp', '0013_alter_users_is_staff_alter_users_is_superuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='is_superuser',
            field=models.BooleanField(default=True),
        ),
    ]
