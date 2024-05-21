import json
import os
import shutil
from datetime import datetime
from pathlib import Path

import pytest
from django.conf import settings
from django.core.management import call_command
from freezegun import freeze_time
from import_export.exceptions import ImportError as IEImportError

from helpers.base import BaseTestCase
from test_app.models import Article, Category, Item, Post


class ExportCMSDataTests(BaseTestCase):
    reset_sequences = True

    def setUp(self):
        self.data_dir: Path = settings.BASE_DIR / "test_commands/data"
        self.expected_data_dir = self.data_dir / "expected_dir"
        self.expected_data_zip = self.data_dir / "expected_data.zip"

        self.corrupted_data_dir = self.data_dir / "corrupted_dir"

        self.result_dir = self.data_dir / "results"

    def tearDown(self):
        """Comment out this tear down to keep the results for comparison."""
        if self.result_dir.exists():
            shutil.rmtree(self.result_dir)

    def get_folder_contents(self, folder_path):
        res = {}
        for path, _sub_dirs, files in os.walk(folder_path):
            for name in files:
                rel_dir = os.path.relpath(path, folder_path)
                rel_file = os.path.join(rel_dir, name)
                ful_path = os.path.join(path, name)
                res[rel_file] = json.loads(self.get_file_data(ful_path))

        return res

    def get_file_data(self, file_path):
        with open(file_path) as f:
            return f.read()

    def compare_folder(self, folder1, folder2):
        folder_1_contents = self.get_folder_contents(folder1)
        folder_2_contents = self.get_folder_contents(folder2)
        assert folder_1_contents == folder_2_contents

    def test_import_export_cms_data(self):
        with freeze_time("2012-01-14 12:00:01"):
            now = datetime.now().strftime("%Y%m%d-%H%M%S")
            call_command("import_cms_data", "test_app", input=self.expected_data_dir)

            assert Post.objects.count() == 3
            assert Article.objects.count() == 3
            assert Item.objects.count() == 9

            call_command("export_cms_data", "test_app", output=self.result_dir)
            result = self.result_dir / now

            self.compare_folder(self.expected_data_dir, result)

    def test_import_export_cms_zip_data(self):
        with freeze_time("2012-01-14 12:00:01"):
            now = datetime.now().strftime("%Y%m%d-%H%M%S")
            call_command("import_cms_data", "test_app", input=self.expected_data_zip)

            assert Post.objects.count() == 3
            assert Article.objects.count() == 3
            assert Item.objects.count() == 9

            call_command(
                "export_cms_data", "test_app", output=self.result_dir, compress=True
            )
            result = self.result_dir / f"{now}.zip"

            temp_extracted_result_zip = self.result_dir / "extracted" / "result"
            temp_extracted_expected_zip = self.result_dir / "extracted" / "expected"

            shutil.unpack_archive(result, temp_extracted_result_zip)
            shutil.unpack_archive(self.expected_data_zip, temp_extracted_expected_zip)

            self.compare_folder(temp_extracted_result_zip, temp_extracted_expected_zip)

    def test_invalid_import_data(self):
        with pytest.raises(shutil.ReadError, match=r"is not a zip file"):
            call_command(
                "import_cms_data", "test_app", input=self.data_dir / "invalid_data.txt"
            )

    def test_atomic_import(self):
        with freeze_time("2012-01-14 12:00:01"):
            call_command("import_cms_data", "test_app", input=self.expected_data_dir)

            assert Post.objects.count() == 3
            assert Category.objects.count() == 3
            assert Article.objects.count() == 3
            assert Item.objects.count() == 9

            with pytest.raises(IEImportError):
                call_command(
                    "import_cms_data", "test_app", input=self.corrupted_data_dir
                )

            assert Post.objects.count() == 3
            assert Category.objects.count() == 3
