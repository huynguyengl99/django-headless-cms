from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("astrowind_posts", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="awpost",
            options={
                "ordering": [
                    models.OrderBy(
                        models.F("publish_date"), descending=True, nulls_first=True
                    ),
                    "-created_date",
                ]
            },
        ),
        migrations.RenameField(
            model_name="awpost",
            old_name="published_date",
            new_name="publish_date",
        ),
        migrations.AlterIndexTogether(
            name="awpost",
            index_together={("publish_date", "created_date")},
        ),
    ]
