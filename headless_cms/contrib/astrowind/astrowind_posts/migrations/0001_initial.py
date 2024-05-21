# Generated by Django 4.2.11 on 2024-05-21 15:07

import django.db.models.deletion
import localized_fields.fields.char_field
import localized_fields.fields.file_field
import localized_fields.fields.text_field
import localized_fields.mixins
import psqlextra.manager.manager
from django.db import migrations, models

import headless_cms.fields.martor_field
import headless_cms.fields.slug_field


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("astrowind_metadata", "0001_initial"),
        ("reversion", "0002_add_index_on_version_for_content_type_and_db"),
    ]

    operations = [
        migrations.CreateModel(
            name="AWCategory",
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
                    "title",
                    localized_fields.fields.text_field.LocalizedTextField(
                        blank=True, null=True, required=[]
                    ),
                ),
                (
                    "slug",
                    headless_cms.fields.slug_field.LocalizedUniqueNormalizedSlugField(
                        blank=True,
                        include_time=False,
                        null=True,
                        populate_from="title",
                        required=[],
                        uniqueness=["en", "vi", "zh", "ar"],
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
        migrations.CreateModel(
            name="AWPost",
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
                    "title",
                    localized_fields.fields.text_field.LocalizedTextField(
                        blank=True, null=True, required=[]
                    ),
                ),
                (
                    "slug",
                    headless_cms.fields.slug_field.LocalizedUniqueNormalizedSlugField(
                        blank=True,
                        include_time=False,
                        null=True,
                        populate_from="title",
                        required=[],
                        uniqueness=["en", "vi", "zh", "ar"],
                    ),
                ),
                (
                    "excerpt",
                    localized_fields.fields.text_field.LocalizedTextField(
                        blank=True, null=True, required=[]
                    ),
                ),
                ("draft", models.BooleanField(default=False)),
                (
                    "author",
                    localized_fields.fields.char_field.LocalizedCharField(
                        blank=True, null=True, required=[]
                    ),
                ),
                (
                    "content",
                    headless_cms.fields.martor_field.LocalizedMartorField(
                        blank=True, default=dict, null=True, required=[]
                    ),
                ),
                ("publish_date", models.DateTimeField(blank=True, null=True)),
                ("updated_date", models.DateTimeField()),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="posts",
                        to="astrowind_posts.awcategory",
                    ),
                ),
            ],
            options={
                "ordering": [
                    models.OrderBy(
                        models.F("publish_date"), descending=True, nulls_first=True
                    ),
                    "-created_date",
                ],
            },
            bases=(localized_fields.mixins.AtomicSlugRetryMixin, models.Model),
            managers=[
                ("objects", psqlextra.manager.manager.PostgresManager()),
            ],
        ),
        migrations.CreateModel(
            name="AWRelatedPost",
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
                    "related_post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="related_through",
                        to="astrowind_posts.awpost",
                    ),
                ),
                (
                    "source_post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="source_through",
                        to="astrowind_posts.awpost",
                    ),
                ),
            ],
            options={
                "ordering": ["position"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="AWPostTag",
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
                    "title",
                    localized_fields.fields.text_field.LocalizedTextField(
                        blank=True, null=True, required=[]
                    ),
                ),
                (
                    "slug",
                    headless_cms.fields.slug_field.LocalizedUniqueNormalizedSlugField(
                        blank=True,
                        include_time=False,
                        null=True,
                        populate_from="title",
                        required=[],
                        uniqueness=["en", "vi", "zh", "ar"],
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
        migrations.CreateModel(
            name="AWPostImage",
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
        migrations.AddField(
            model_name="awpost",
            name="image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="posts",
                to="astrowind_posts.awpostimage",
            ),
        ),
        migrations.AddField(
            model_name="awpost",
            name="metadata",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="astrowind_metadata.awmetadata",
            ),
        ),
        migrations.AddField(
            model_name="awpost",
            name="published_version",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="reversion.version",
            ),
        ),
        migrations.AddField(
            model_name="awpost",
            name="related_posts",
            field=models.ManyToManyField(
                blank=True,
                through="astrowind_posts.AWRelatedPost",
                to="astrowind_posts.awpost",
            ),
        ),
        migrations.AddField(
            model_name="awpost",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="posts", to="astrowind_posts.awposttag"
            ),
        ),
        migrations.AlterIndexTogether(
            name="awpost",
            index_together={("publish_date", "created_date")},
        ),
    ]
