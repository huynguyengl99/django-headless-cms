import django.db.models.deletion
import localized_fields.fields.text_field
import localized_fields.mixins
import psqlextra.manager.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reversion", "0002_add_index_on_version_for_content_type_and_db"),
        ("astrowind_posts", "0004_awposttag"),
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
    ]
