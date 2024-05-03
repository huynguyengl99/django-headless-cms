# Generated by Django 4.2.11 on 2024-05-01 17:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("astrowind_widgets", "0037_alter_awcontent_options_and_more"),
        ("astrowind_pages", "0009_awcontactpage"),
    ]

    operations = [
        migrations.CreateModel(
            name="AWIndexPageContentThrough",
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
                    "content",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="astrowind_widgets.awcontent",
                    ),
                ),
                (
                    "index_page",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="astrowind_pages.awindexpage",
                    ),
                ),
            ],
            options={
                "ordering": ["position"],
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="awindexpage",
            name="contents",
            field=models.ManyToManyField(
                blank=True,
                related_name="index_page",
                through="astrowind_pages.AWIndexPageContentThrough",
                to="astrowind_widgets.awcontent",
            ),
        ),
    ]