# Generated by Django 4.2.11 on 2024-05-01 13:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("astrowind_widgets", "0033_remove_awdisclaimer_autocomplete_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="awfooterlinkitem",
            options={},
        ),
        migrations.RemoveField(
            model_name="awfooterlinkitem",
            name="footer_links",
        ),
        migrations.RemoveField(
            model_name="awfooterlinkitem",
            name="position",
        ),
        migrations.CreateModel(
            name="AWFooterLinkThrough",
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
                    "footer_link",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="astrowind_widgets.awfooterlink",
                    ),
                ),
                (
                    "footer_link_item",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="astrowind_widgets.awfooterlinkitem",
                    ),
                ),
            ],
            options={
                "ordering": ["position"],
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="awfooterlink",
            name="links",
            field=models.ManyToManyField(
                blank=True,
                related_name="links_footers",
                through="astrowind_widgets.AWFooterLinkThrough",
                to="astrowind_widgets.awfooterlinkitem",
            ),
        ),
    ]
