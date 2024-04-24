import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("astrowind_posts", "0005_awcategory"),
    ]

    operations = [
        migrations.AddField(
            model_name="awpost",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="posts",
                to="astrowind_posts.awcategory",
            ),
        ),
        migrations.AddField(
            model_name="awpost",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="posts", to="astrowind_posts.awposttag"
            ),
        ),
    ]
