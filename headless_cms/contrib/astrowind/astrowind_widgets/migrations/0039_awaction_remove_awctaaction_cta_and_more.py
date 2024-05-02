import django.db.models.deletion
import localized_fields.fields.char_field
import localized_fields.mixins
import psqlextra.manager.manager
from django.db import migrations, models

import headless_cms.fields.url_field


class Migration(migrations.Migration):

    dependencies = [
        ("reversion", "0002_add_index_on_version_for_content_type_and_db"),
        (
            "astrowind_widgets",
            "0038_alter_awstatitem_options_remove_awstatitem_position_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="AWAction",
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
                    "variant",
                    models.CharField(
                        choices=[
                            ("primary", "Primary"),
                            ("secondary", "Secondary"),
                            ("tertiary", "Tertiary"),
                            ("link", "Link"),
                        ],
                        default="secondary",
                    ),
                ),
                ("target", models.CharField(blank=True, default="")),
                (
                    "text",
                    localized_fields.fields.char_field.LocalizedCharField(
                        blank=True, null=True, required=[]
                    ),
                ),
                (
                    "href",
                    headless_cms.fields.url_field.AutoLanguageUrlField(
                        blank=True, default=""
                    ),
                ),
                ("icon", models.CharField(blank=True, default="")),
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
            model_name="awctaaction",
            name="cta",
        ),
        migrations.RemoveField(
            model_name="awctaaction",
            name="published_version",
        ),
        migrations.RemoveField(
            model_name="awheaderaction",
            name="published_version",
        ),
        migrations.RemoveField(
            model_name="awheaderactionthrough",
            name="header",
        ),
        migrations.RemoveField(
            model_name="awheaderactionthrough",
            name="header_action",
        ),
        migrations.RemoveField(
            model_name="awheroaction",
            name="hero",
        ),
        migrations.RemoveField(
            model_name="awheroaction",
            name="published_version",
        ),
        migrations.RemoveField(
            model_name="awherotextaction",
            name="published_version",
        ),
        migrations.RemoveField(
            model_name="awpriceitemaction",
            name="published_version",
        ),
        migrations.RemoveField(
            model_name="awstep2action",
            name="published_version",
        ),
        migrations.RemoveField(
            model_name="awtestimonialaction",
            name="published_version",
        ),
        migrations.RemoveField(
            model_name="awcontent",
            name="call_to_action",
        ),
        migrations.RemoveField(
            model_name="awheader",
            name="actions",
        ),
        migrations.RemoveField(
            model_name="awherotext",
            name="call_to_action",
        ),
        migrations.RemoveField(
            model_name="awherotext",
            name="call_to_action2",
        ),
        migrations.RemoveField(
            model_name="awpriceitem",
            name="call_to_action",
        ),
        migrations.RemoveField(
            model_name="awstep2",
            name="call_to_action",
        ),
        migrations.RemoveField(
            model_name="awtestimonial",
            name="call_to_action",
        ),
        migrations.DeleteModel(
            name="AWContentAction",
        ),
        migrations.DeleteModel(
            name="AWCTAAction",
        ),
        migrations.DeleteModel(
            name="AWHeaderAction",
        ),
        migrations.DeleteModel(
            name="AWHeaderActionThrough",
        ),
        migrations.DeleteModel(
            name="AWHeroAction",
        ),
        migrations.DeleteModel(
            name="AWHeroTextAction",
        ),
        migrations.DeleteModel(
            name="AWPriceItemAction",
        ),
        migrations.DeleteModel(
            name="AWStep2Action",
        ),
        migrations.DeleteModel(
            name="AWTestimonialAction",
        ),
    ]
