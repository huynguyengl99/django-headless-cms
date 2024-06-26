# Generated by Django 4.2.13 on 2024-06-04 18:00

import django.db.models.deletion
import localized_fields.fields.char_field
import localized_fields.fields.text_field
import localized_fields.mixins
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("reversion", "0002_add_index_on_version_for_content_type_and_db"),
    ]

    operations = [
        migrations.CreateModel(
            name="AWMetadataImage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "url",
                    localized_fields.fields.char_field.LocalizedCharField(
                        blank=True, null=True, required=[]
                    ),
                ),
                ("width", models.IntegerField(default=0)),
                ("height", models.IntegerField(default=0)),
                (
                    "published_version",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="reversion.version",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(localized_fields.mixins.AtomicSlugRetryMixin, models.Model),
        ),
        migrations.CreateModel(
            name="AWMetaDataTwitter",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "handle",
                    localized_fields.fields.char_field.LocalizedCharField(
                        blank=True, null=True, required=[]
                    ),
                ),
                (
                    "site",
                    localized_fields.fields.char_field.LocalizedCharField(
                        blank=True, null=True, required=[]
                    ),
                ),
                (
                    "card_type",
                    localized_fields.fields.char_field.LocalizedCharField(
                        blank=True, null=True, required=[]
                    ),
                ),
                (
                    "published_version",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="reversion.version",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(localized_fields.mixins.AtomicSlugRetryMixin, models.Model),
        ),
        migrations.CreateModel(
            name="AWMetadataRobot",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("index", models.BooleanField(default=False)),
                ("follow", models.BooleanField(default=False)),
                (
                    "published_version",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="reversion.version",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(localized_fields.mixins.AtomicSlugRetryMixin, models.Model),
        ),
        migrations.CreateModel(
            name="AWMetaDataOpenGraph",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "url",
                    localized_fields.fields.char_field.LocalizedCharField(
                        blank=True, null=True, required=[]
                    ),
                ),
                (
                    "site_name",
                    localized_fields.fields.char_field.LocalizedCharField(
                        blank=True, null=True, required=[]
                    ),
                ),
                (
                    "locale",
                    localized_fields.fields.char_field.LocalizedCharField(
                        blank=True, null=True, required=[]
                    ),
                ),
                ("type", models.CharField(blank=True, default="")),
                (
                    "images",
                    models.ManyToManyField(
                        related_name="metadata_open_graphs",
                        to="astrowind_metadata.awmetadataimage",
                    ),
                ),
                (
                    "published_version",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="reversion.version",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(localized_fields.mixins.AtomicSlugRetryMixin, models.Model),
        ),
        migrations.CreateModel(
            name="AWMetadata",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    localized_fields.fields.text_field.LocalizedTextField(
                        blank=True, null=True, required=[]
                    ),
                ),
                (
                    "title_template",
                    localized_fields.fields.text_field.LocalizedTextField(
                        blank=True,
                        default=dict,
                        help_text="Title template (default should be %s - {title}), used for default site metadata.",
                        null=True,
                        required=[],
                    ),
                ),
                (
                    "description",
                    localized_fields.fields.text_field.LocalizedTextField(
                        blank=True, null=True, required=[]
                    ),
                ),
                (
                    "canonical",
                    localized_fields.fields.char_field.LocalizedCharField(
                        blank=True, null=True, required=[]
                    ),
                ),
                ("ignore_title_template", models.BooleanField(default=False)),
                (
                    "open_graph",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="metadata",
                        to="astrowind_metadata.awmetadataopengraph",
                    ),
                ),
                (
                    "published_version",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="reversion.version",
                    ),
                ),
                (
                    "robots",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="metadata",
                        to="astrowind_metadata.awmetadatarobot",
                    ),
                ),
                (
                    "twitter",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="metadata",
                        to="astrowind_metadata.awmetadatatwitter",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(localized_fields.mixins.AtomicSlugRetryMixin, models.Model),
        ),
    ]
