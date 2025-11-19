import cgi
import shutil
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, urlretrieve

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models, transaction
from django.db.models import ForeignKey, ManyToManyField
from reversion.management.commands import BaseRevisionCommand
from tablib import Dataset

from headless_cms.models import LocalizedPublicationModel
from headless_cms.utils.custom_import_export import override_modelresource_factory


class Command(BaseRevisionCommand):
    """
    Imports data recursively of a Django app from JSON files.

    Usage:
        python manage.py import_cms_data [app_label ...] [--using DATABASE] [--model-db DATABASE] [--input DIRECTORY_OR_FILE] [--cf FORMAT]

    Options:
        app_label: Optional app_label or app_label.model_name list.
        --using: The database to query for revision data.
        --model-db: The database to query for model data.
        --input: Directory or compression file to import data from.
        --cf, --compress-format: Compression format (default is zip).
    """

    help = "Import data recursively of a Django app from JSON files."

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--input",
            required=True,
            type=str,
            help="Directory or compression file to import data from.",
        )
        parser.add_argument(
            "--cf",
            "--compress-format",
            default="zip",
            type=str,
            help="Compression format.",
        )

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self.imported_models = set()
        self.input_data_path = ""
        self.temp_download_dir = None
        self.data_input_dir = None
        self.temp_extracted_input_dir = None
        self.verbosity = 0

    def import_model(self, model: type[models.Model]) -> None:
        if model in self.imported_models:
            return
        self.imported_models.add(model)
        model_fields = model._meta.get_fields()

        through_models = []
        for field in model_fields:
            if isinstance(field, GenericRelation | ForeignKey) and issubclass(
                field.related_model, LocalizedPublicationModel
            ):
                self.import_model(field.related_model)
            elif (isinstance(field, ManyToManyField)) and issubclass(
                field.related_model, LocalizedPublicationModel
            ):
                self.import_model(field.related_model)
                through = getattr(model, field.name).through
                through_models.append(through)

        if self.verbosity >= 1:
            self.stdout.write(f"Import data for {model._meta.object_name}")

        file_to_import: Path = (
            self.data_input_dir
            / model._meta.app_label
            / f"{model._meta.object_name}.json"
        )

        if file_to_import.exists():
            with open(file_to_import) as fh:
                imported_data = Dataset().load(fh)

            import_model_resource = override_modelresource_factory(
                model, exclude_m2m=True
            )
            import_model = import_model_resource()

            import_model.import_data(imported_data, raise_errors=True)

        for through in through_models:
            self.import_model(through)

    def check_input_path(self, input_path):
        if str(input_path).startswith("https://"):
            self.temp_download_dir = Path("temp_import/")
            self.temp_download_dir.mkdir(parents=True, exist_ok=True)
            remote_file = urlopen(input_path)
            content_disposition = remote_file.info()["Content-Disposition"]
            if content_disposition:
                _, params = cgi.parse_header(content_disposition)
                filename = params["filename"]
            else:
                filename = input_path.rsplit("/", 1)[-1]  # infer from url

            if "." not in filename:
                raise ValueError(f"URL must download a zip file, not {filename}")

            temp_input_data_path = self.temp_download_dir / filename
            urlretrieve(input_path, temp_input_data_path)

            input_path = temp_input_data_path

        return input_path

    def prepare_for_input(self, input_path, compress_format):
        input_path = self.check_input_path(input_path)

        self.input_data_path = Path(input_path)

        if self.input_data_path.is_dir():
            self.data_input_dir = Path(self.input_data_path)
        else:
            self.temp_extracted_input_dir = Path("temp-extracted-input")
            self.data_input_dir = (
                self.temp_extracted_input_dir / datetime.now().strftime("%Y%m%d-%H%M%S")
            )
            self.uncompress_input(compress_format)

    def handle(self, *app_labels, **options):
        self.prepare_for_input(options["input"], options["cf"])

        self.verbosity = options["verbosity"]

        with transaction.atomic():
            for model in self.get_models(options):
                if not issubclass(model, LocalizedPublicationModel):
                    continue

                self.import_model(model)

        self.clean_up()

    def uncompress_input(self, compress_format):
        shutil.unpack_archive(
            self.input_data_path, self.data_input_dir, compress_format
        )

    def clean_up(self):
        if self.temp_extracted_input_dir:
            shutil.rmtree(self.temp_extracted_input_dir)

        if self.temp_download_dir:
            shutil.rmtree(self.temp_download_dir)
