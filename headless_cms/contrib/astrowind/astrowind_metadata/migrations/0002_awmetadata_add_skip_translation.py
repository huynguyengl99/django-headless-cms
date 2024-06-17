from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("astrowind_metadata", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="awmetadata",
            name="skip_translation",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="awmetadataimage",
            name="skip_translation",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="awmetadataopengraph",
            name="skip_translation",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="awmetadatarobot",
            name="skip_translation",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="awmetadatatwitter",
            name="skip_translation",
            field=models.BooleanField(default=False),
        ),
    ]
