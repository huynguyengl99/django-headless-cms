# Generated by Django 4.2.11 on 2024-05-19 14:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("astrowind_metadata", "0001_initial"),
        ("astrowind_pages", "0015_awsite_philosophy_awsite_philosophy_text"),
    ]

    operations = [
        migrations.AddField(
            model_name="awsite",
            name="default_metadata",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="astrowind_metadata.awmetadata",
            ),
        ),
    ]
