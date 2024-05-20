import shutil
from datetime import datetime
from pathlib import Path

from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import ForeignKey, ManyToManyField
from reversion.management.commands import BaseRevisionCommand
from tablib import Dataset

from headless_cms.models import LocalizedPublicationModel
from headless_cms.utils.custom_import_export import override_modelresource_factory


class Command(BaseRevisionCommand):
    help = "Export data recursively of a Django app into JSON files."

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
        self.input_data_path = None
        self.data_input_dir = None
        self.temp_extracted_input_dir = None
        self.verbosity = 0

    def import_model(self, model):
        if model in self.imported_models:
            return
        self.imported_models.add(model)
        model_fields = model._meta.get_fields()
        for field in model_fields:
            if isinstance(field, (GenericRelation, ForeignKey)) and issubclass(
                field.related_model, LocalizedPublicationModel
            ):
                self.import_model(field.related_model)
            elif (isinstance(field, ManyToManyField)) and issubclass(
                field.related_model, LocalizedPublicationModel
            ):
                self.import_model(field.related_model)
                through = getattr(model, field.name).through
                self.import_model(through)

        if self.verbosity >= 1:
            self.stdout.write(f"Import data for {model._meta.object_name}")

        file_to_import: Path = (
            self.data_input_dir
            / model._meta.app_label
            / f"{model._meta.object_name}.json"
        )
        with open(file_to_import) as fh:
            imported_data = Dataset().load(fh)

        import_model_resource = override_modelresource_factory(model)
        import_model = import_model_resource()

        import_model.import_data(imported_data)

    def handle(self, *app_labels, **options):
        self.input_data_path = Path(options["input"])

        if self.input_data_path.is_dir():
            self.data_input_dir = Path(self.input_data_path)
        elif self.input_data_path.is_file():
            self.temp_extracted_input_dir = Path("temp-extracted-input")
            self.data_input_dir = (
                self.temp_extracted_input_dir / datetime.now().strftime("%Y%m%d-%H%M%S")
            )
            self.uncompress_input(options["cf"])
        else:
            raise ValueError(f"Invalid input: {self.input_data_path}")

        self.verbosity = options["verbosity"]

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
