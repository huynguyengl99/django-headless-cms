from django.apps import apps
from django.core.management import call_command
from reversion.management.commands import BaseRevisionCommand

from headless_cms.models import LocalizedPublicationModel


class Command(BaseRevisionCommand):
    """
    Populates Astrowind data.

    Usage:
        python manage.py populate_aw_data
    """

    help = "Populate astrowind data."

    def handle(self, *app_labels, **options):
        populate_apps = (
            "astrowind_posts",
            "astrowind_pages",
        )
        call_command(
            "import_cms_data",
            *populate_apps,
            input="https://raw.githubusercontent.com/huynguyengl99/dj-hcms-data/main/data/astrowind/astrowind.zip",
        )
        page_models = []
        for app_name in populate_apps:
            page_models.extend(
                app for app in apps.get_app_config(app_name).get_models()
            )
        print("Publish Astrowind pages and posts.")
        for page_model in page_models:
            for page in page_model.objects.all():
                if isinstance(page, LocalizedPublicationModel):
                    page: LocalizedPublicationModel
                    page.recursively_publish()
