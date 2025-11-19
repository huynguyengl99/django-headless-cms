import json
import shutil
from datetime import datetime
from pathlib import Path

from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import ForeignKey, ManyToManyField
from reversion.management.commands import BaseRevisionCommand

from headless_cms.models import LocalizedPublicationModel
from headless_cms.utils.custom_import_export import override_modelresource_factory


class Command(BaseRevisionCommand):
    """
    Exports data recursively of a Django app into JSON files.

    Usage:
        python manage.py export_cms_data [app_label ...] [--using DATABASE] [--model-db DATABASE] [--output DIRECTORY] [--compress] [--cf FORMAT]

    Options:
        app_label: Optional app_label or app_label.model_name list.
        --using: The database to query for revision data.
        --model-db: The database to query for model data.
        --output: Export data to this directory.
        --compress: Compress data.
        --cf, --compress-format: Compression format (default is zip).
    """

    help = "Export data recursively of a Django app into JSON files."

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--output",
            default="exported_data",
            type=str,
            help="Export data to this directory.",
        )
        parser.add_argument(
            "--cf",
            "--compress-format",
            default="zip",
            type=str,
            help="Compression format.",
        )
        parser.add_argument(
            "--compress",
            default=False,
            action="store_true",
            help="Compress data",
        )

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self.exported_models = set()
        self.base_output_dir = None
        self.data_output_dir = None
        self.current_time = None
        self.should_compress = False
        self.verbosity = 0

    def export_model(self, model):
        if model in self.exported_models:
            return
        self.exported_models.add(model)
        model_fields = model._meta.get_fields()
        for field in model_fields:
            if isinstance(field, GenericRelation | ForeignKey) and issubclass(
                field.related_model, LocalizedPublicationModel
            ):
                self.export_model(field.related_model)
            elif (isinstance(field, ManyToManyField)) and issubclass(
                field.related_model, LocalizedPublicationModel
            ):
                self.export_model(field.related_model)
                through = getattr(model, field.name).through
                self.export_model(through)

        export_model_resource = override_modelresource_factory(model, exclude_m2m=True)
        export_model = export_model_resource()

        data = export_model.export()
        if self.verbosity >= 1:
            self.stdout.write(f"Export data for {model._meta.object_name}")

        dest_dir: Path = self.data_output_dir / model._meta.app_label
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_file: Path = dest_dir / f"{model._meta.object_name}.json"

        with open(dest_file, "w") as f:
            f.write(
                json.dumps(data.dict, indent=2)
                if not self.should_compress
                else data.json
            )

    def handle(self, *app_labels, **options):
        self.base_output_dir = Path(options["output"])
        self.current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.data_output_dir = self.base_output_dir / self.current_time

        print(f"Export data to {self.data_output_dir}")

        self.should_compress = options["compress"]

        if not self.data_output_dir.exists():
            self.data_output_dir.mkdir(parents=True, exist_ok=True)

        self.verbosity = options["verbosity"]

        for model in self.get_models(options):
            if not issubclass(model, LocalizedPublicationModel):
                continue

            self.export_model(model)

        if self.should_compress:
            self.compress_output(options["cf"])

        self.clean_up()

    def compress_output(self, compress_format):
        dest_file = self.base_output_dir / f"{self.current_time}"
        shutil.make_archive(dest_file, compress_format, self.data_output_dir)

    def clean_up(self):
        if self.should_compress:
            shutil.rmtree(self.data_output_dir)
