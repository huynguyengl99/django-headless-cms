from datetime import timedelta

from django.db import models, router, transaction
from django.utils import timezone
from reversion.management.commands import BaseRevisionCommand
from reversion.models import Revision

from headless_cms.models import LocalizedPublicationModel


class Command(BaseRevisionCommand):
    """
    Deletes outdated drafts.

    Usage:
        python manage.py clean_outdated_drafts [app_label ...] [--using DATABASE] [--model-db DATABASE] [--days DAYS]

    Options:
        app_label: Optional app_label or app_label.model_name list.
        --using: The database to query for revision data.
        --model-db: The database to query for model data.
        --days: Delete only revisions older than the specified number of days.
    """

    help = "Deletes outdated drafts."

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--days",
            default=0,
            type=int,
            help="Delete only revisions older than the specified number of days.",
        )

    def handle(self, *app_labels, **options):
        verbosity = options["verbosity"]
        using = options["using"]
        days = options["days"]
        using = using or router.db_for_write(Revision)
        with transaction.atomic(using=using):
            revision_query = models.Q()
            remove_revision_ids = set()
            can_delete = False
            for model in self.get_models(options):
                if not issubclass(model, LocalizedPublicationModel):
                    continue
                if verbosity >= 1:
                    self.stdout.write(
                        f"Finding outdated draft revisions for {model._meta.verbose_name}"
                    )

                published_objs = (
                    model.objects.using(using)
                    .prefetch_related("versions")
                    .filter(published_version_id__isnull=False)
                )
                for obj in published_objs:
                    remove_revision_ids.update(
                        obj.versions.filter(id__lt=obj.published_version_id)
                        .values_list("revision_id", flat=True)
                        .iterator()
                    )

                revision_query |= models.Q(pk__in=remove_revision_ids)
                can_delete = True
            if can_delete:
                revisions_to_delete = (
                    Revision.objects.using(using)
                    .filter(
                        revision_query,
                        date_created__lt=timezone.now() - timedelta(days=days),
                    )
                    .order_by()
                )
            else:
                revisions_to_delete = Revision.objects.using(using).none()
            if verbosity >= 1:
                self.stdout.write(
                    f"Deleting {revisions_to_delete.count()} revisions..."
                )
            revisions_to_delete.delete()
