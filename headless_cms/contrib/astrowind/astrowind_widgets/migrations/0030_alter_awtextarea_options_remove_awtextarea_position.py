# Generated by Django 4.2.11 on 2024-04-21 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("astrowind_widgets", "0029_remove_awcontact_inputs_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="awtextarea",
            options={},
        ),
        migrations.RemoveField(
            model_name="awtextarea",
            name="position",
        ),
    ]