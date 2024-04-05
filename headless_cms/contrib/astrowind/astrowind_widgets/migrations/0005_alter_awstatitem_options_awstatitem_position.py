# Generated by Django 4.2.11 on 2024-04-05 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("astrowind_widgets", "0004_awcontent_content"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="awstatitem",
            options={"ordering": ["position"]},
        ),
        migrations.AddField(
            model_name="awstatitem",
            name="position",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
