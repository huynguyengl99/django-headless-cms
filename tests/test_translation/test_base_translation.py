from unittest.mock import MagicMock

from django.conf import settings
from headless_cms.auto_translate import BaseTranslate

from helpers.base import BaseTestCase
from test_app.factories import PostFactory
from test_app.models import Post


class TestBaseTranslate(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.instance: Post = PostFactory()
        self.translate = BaseTranslate(self.instance)

        def batch_translate(raw):
            res = {}
            for language, obj_to_trans in raw.items():
                res[language] = {k: language + "-" + v for k, v in obj_to_trans.items()}
            return res

        self.batch_translate = batch_translate
        self.mock_batch_translate = MagicMock(side_effect=batch_translate)

    def test_translate_base_no_implemented(self):
        result = self.translate.translate("en", "Hello, World!")
        assert result == "Hello, World!"

    def test_process(self):
        self.translate.translate = MagicMock(side_effect=lambda lang, text: text[::-1])
        self.translate.batch_translate = MagicMock(return_value=["Hello, World!"])

        self.translate.process()

        self.translate.translate.assert_called()
        self.translate.batch_translate.assert_not_called()

    def test_process_batch_translate(self):
        data = {settings.LANGUAGE_CODE: "value"}

        self.instance: Post = PostFactory(title=data, description=data, body=data)
        self.translate = BaseTranslate(self.instance)

        self.translate.batch_translate = self.mock_batch_translate
        self.translate.can_batch_translate = True
        self.translate.process()

        obj_to_translate = {
            "title": getattr(self.instance.title, settings.LANGUAGE_CODE),
            "description": getattr(self.instance.description, settings.LANGUAGE_CODE),
            "body": getattr(self.instance.body, settings.LANGUAGE_CODE),
        }

        batches = {
            "ro": obj_to_translate,
            "vi": obj_to_translate,
        }

        self.translate.batch_translate.assert_called_with(batches)

        self.instance.refresh_from_db()

        expected_batch_translate = self.batch_translate(batches)
        for lang, _lang_name in settings.LANGUAGES:
            if lang == settings.LANGUAGE_CODE:
                continue
            expected_obj = expected_batch_translate[lang]
            assert getattr(self.instance.title, lang) == expected_obj["title"]
            assert (
                getattr(self.instance.description, lang) == expected_obj["description"]
            )
            assert getattr(self.instance.body, lang) == expected_obj["body"]

    def test_process_without_force_and_fulfilled(self):
        data = {}
        for lang, _code in settings.LANGUAGES:
            data[lang] = "value"

        self.instance: Post = PostFactory(title=data, description=data, body=data)
        self.translate = BaseTranslate(self.instance)

        self.translate.translate = MagicMock(side_effect=lambda lang, text: text[::-1])
        self.translate.batch_translate = MagicMock(return_value=["Hello, World!"])

        self.translate.process()

        self.translate.translate.assert_not_called()

    def test_process_with_force_and_fulfilled(self):
        data = {}
        for lang, _code in settings.LANGUAGES:
            data[lang] = "value"

        self.instance: Post = PostFactory(title=data, description=data, body=data)
        self.translate = BaseTranslate(self.instance)

        self.translate.translate = MagicMock(side_effect=lambda lang, text: text[::-1])
        self.translate.batch_translate = MagicMock(return_value=["Hello, World!"])

        self.translate.process(force=True)

        self.translate.translate.assert_called()

    def test_process_batch_translate_without_force_and_fulfilled(self):
        data = {}
        for lang, _code in settings.LANGUAGES:
            data[lang] = "value"

        self.instance: Post = PostFactory(title=data, description=data, body=data)
        self.translate = BaseTranslate(self.instance)

        self.translate.translate = MagicMock(side_effect=lambda lang, text: text[::-1])

        self.translate.batch_translate = MagicMock(side_effect=lambda x: x)

        self.translate.can_batch_translate = True
        self.translate.process()

        self.translate.batch_translate.assert_called_with({})

    def test_process_batch_translate_with_force_and_fulfilled(self):
        data = {}
        for lang, _lang_name in settings.LANGUAGES:
            data[lang] = "value"

        self.instance: Post = PostFactory(title=data, description=data, body=data)
        self.translate = BaseTranslate(self.instance)

        self.translate.translate = MagicMock(side_effect=lambda lang, text: text[::-1])

        self.translate.batch_translate = self.mock_batch_translate

        self.translate.can_batch_translate = True
        self.translate.process(force=True)
        obj_to_translate = {
            "title": getattr(self.instance.title, settings.LANGUAGE_CODE),
            "description": getattr(self.instance.description, settings.LANGUAGE_CODE),
            "body": getattr(self.instance.body, settings.LANGUAGE_CODE),
        }

        batches = {
            "ro": obj_to_translate,
            "vi": obj_to_translate,
        }
        self.translate.batch_translate.assert_called_with(batches)

        self.instance.refresh_from_db()

        expected_batch_translate = self.batch_translate(batches)
        for lang, _lang_name in settings.LANGUAGES:
            if lang == settings.LANGUAGE_CODE:
                continue
            expected_obj = expected_batch_translate[lang]
            assert getattr(self.instance.title, lang) == expected_obj["title"]
            assert (
                getattr(self.instance.description, lang) == expected_obj["description"]
            )
            assert getattr(self.instance.body, lang) == expected_obj["body"]
