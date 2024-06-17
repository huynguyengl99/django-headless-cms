from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("astrowind_pages", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="awaboutpage",
            name="skip_translation",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="awcontactpage",
            name="skip_translation",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="awindexpage",
            name="skip_translation",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="awpostpage",
            name="skip_translation",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="awpricingpage",
            name="skip_translation",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="awsite",
            name="skip_translation",
            field=models.BooleanField(default=False),
        ),
    ]
