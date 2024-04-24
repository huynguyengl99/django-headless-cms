from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("astrowind_posts", "0002_alter_awpost_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="awpost",
            name="category",
        ),
        migrations.RemoveField(
            model_name="awpost",
            name="tags",
        ),
    ]
