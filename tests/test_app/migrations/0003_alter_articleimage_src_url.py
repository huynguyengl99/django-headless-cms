# Generated by Django 4.2.13 on 2024-06-20 17:22

import headless_cms.fields.url_field
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("test_app", "0002_article_skip_translation_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="articleimage",
            name="src_url",
            field=headless_cms.fields.url_field.LocalizedUrlField(
                blank=True, default=dict, null=True, required=[]
            ),
        ),
    ]
