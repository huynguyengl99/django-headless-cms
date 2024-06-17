from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("astrowind_posts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="awcategory",
            name="skip_translation",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="awpost",
            name="skip_translation",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="awpostimage",
            name="skip_translation",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="awposttag",
            name="skip_translation",
            field=models.BooleanField(default=False),
        ),
    ]
