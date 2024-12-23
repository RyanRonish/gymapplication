# Generated by Django 5.1.3 on 2024-12-06 03:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("gym", "0007_remove_gym_last_updated_alter_gym_is_open"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="github",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="linkedin",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="twitter",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="apartment_number",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="bio",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="profile",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
