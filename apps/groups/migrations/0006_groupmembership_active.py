# Generated by Django 5.2.2 on 2025-06-16 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0005_alter_group_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupmembership',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
