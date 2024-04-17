# Generated by Django 4.2.11 on 2024-04-17 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("astrowind_widgets", "0022_alter_awfooterlinkitem_footer_links"),
    ]

    operations = [
        migrations.AddField(
            model_name="awbrandimage",
            name="src_url",
            field=models.CharField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="awcontentimage",
            name="src_url",
            field=models.CharField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="awheroimage",
            name="src_url",
            field=models.CharField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="awstepimage",
            name="src_url",
            field=models.CharField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="awtestimonialitemimage",
            name="src_url",
            field=models.CharField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="awbrandimage",
            name="src",
            field=models.FileField(blank=True, null=True, upload_to=""),
        ),
        migrations.AlterField(
            model_name="awcontentimage",
            name="src",
            field=models.FileField(blank=True, null=True, upload_to=""),
        ),
        migrations.AlterField(
            model_name="awheroimage",
            name="src",
            field=models.FileField(blank=True, null=True, upload_to=""),
        ),
        migrations.AlterField(
            model_name="awstepimage",
            name="src",
            field=models.FileField(blank=True, null=True, upload_to=""),
        ),
        migrations.AlterField(
            model_name="awtestimonialitemimage",
            name="src",
            field=models.FileField(blank=True, null=True, upload_to=""),
        ),
    ]
