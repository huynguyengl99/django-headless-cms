# Generated by Django 4.2.11 on 2024-05-17 17:22

import localized_fields.fields.text_field
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("astrowind_pages", "0013_awpostpage_blog_text"),
    ]

    operations = [
        migrations.AddField(
            model_name="awsite",
            name="announcement",
            field=localized_fields.fields.text_field.LocalizedTextField(
                blank=True, default=dict, null=True, required=[]
            ),
        ),
    ]
