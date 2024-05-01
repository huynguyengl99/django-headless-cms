# Generated by Django 4.2.11 on 2024-05-01 16:56

import django.db.models.deletion
import localized_fields.fields.char_field
import localized_fields.fields.file_field
import localized_fields.fields.text_field
import localized_fields.mixins
import psqlextra.manager.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reversion", "0002_add_index_on_version_for_content_type_and_db"),
        ("astrowind_widgets", "0034_alter_awfooterlinkitem_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="AWImage",
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
                (
                    "src_file",
                    localized_fields.fields.file_field.LocalizedFileField(
                        blank=True, default=dict, null=True, required=[], upload_to=""
                    ),
                ),
                (
                    "src_url",
                    localized_fields.fields.char_field.LocalizedCharField(
                        blank=True, default=dict, null=True, required=[]
                    ),
                ),
                (
                    "alt",
                    localized_fields.fields.text_field.LocalizedTextField(
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
            managers=[
                ("objects", psqlextra.manager.manager.PostgresManager()),
            ],
        ),
        migrations.RemoveField(
            model_name="awcontentimage",
            name="published_version",
        ),
        migrations.RemoveField(
            model_name="awheroimage",
            name="published_version",
        ),
        migrations.RemoveField(
            model_name="awstepimage",
            name="published_version",
        ),
        migrations.RemoveField(
            model_name="awtestimonialitemimage",
            name="published_version",
        ),
        migrations.RemoveField(
            model_name="awcontent",
            name="image",
        ),
        migrations.RemoveField(
            model_name="awhero",
            name="image",
        ),
        migrations.RemoveField(
            model_name="awstep",
            name="image",
        ),
        migrations.RemoveField(
            model_name="awtestimonialitem",
            name="image",
        ),
        migrations.DeleteModel(
            name="AWBrandImage",
        ),
        migrations.DeleteModel(
            name="AWContentImage",
        ),
        migrations.DeleteModel(
            name="AWHeroImage",
        ),
        migrations.DeleteModel(
            name="AWStepImage",
        ),
        migrations.DeleteModel(
            name="AWTestimonialItemImage",
        ),
    ]
