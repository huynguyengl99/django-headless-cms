# Generated by Django 4.2.11 on 2024-05-18 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("astrowind_posts", "0015_alter_awcategory_slug_alter_awpost_slug_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="awpost",
            name="metadata",
        ),
        migrations.DeleteModel(
            name="AWPostMetadata",
        ),
    ]
