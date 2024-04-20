# Generated by Django 4.2.11 on 2024-04-20 16:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("astrowind_widgets", "0026_alter_awcontentaction_variant_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="awpriceitem",
            name="pricing",
        ),
        migrations.CreateModel(
            name="AWPriceItemThrough",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("position", models.PositiveIntegerField(default=0)),
                (
                    "price_item",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="astrowind_widgets.awpriceitem",
                    ),
                ),
                (
                    "pricing",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="astrowind_widgets.awpricing",
                    ),
                ),
            ],
            options={
                "ordering": ["position"],
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="awpricing",
            name="prices",
            field=models.ManyToManyField(
                blank=True,
                related_name="aw_pricing",
                through="astrowind_widgets.AWPriceItemThrough",
                to="astrowind_widgets.awpriceitem",
            ),
        ),
    ]
