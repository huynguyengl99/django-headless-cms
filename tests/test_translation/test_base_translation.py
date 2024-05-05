from unittest.mock import MagicMock, call

from django.conf import settings
from headless_cms.auto_translate import BaseTranslate
from localized_fields.value import LocalizedValue

from test_app.factories import PostFactory
from test_app.models import Post
from test_utils.base import BaseTestCase


class TestBaseTranslate(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.instance: Post = PostFactory()
        self.translate = BaseTranslate(self.instance)

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

        def batch_translate(trans_lang, trans_obj):
            return {k: trans_lang + "-" + v for k, v in trans_obj.items()}

        self.translate.batch_translate = MagicMock(side_effect=batch_translate)
        self.translate.can_translate_object = True
        self.translate.process()

        obj_to_translate = {
            "title": getattr(self.instance.title, settings.LANGUAGE_CODE),
            "description": getattr(self.instance.description, settings.LANGUAGE_CODE),
            "body": getattr(self.instance.body, settings.LANGUAGE_CODE),
        }

        self.translate.batch_translate.assert_has_calls(
            [
                call("ro", obj_to_translate),
                call("vi", obj_to_translate),
            ],
            True,
        )
        self.instance.refresh_from_db()
        for lang, _lang_name in settings.LANGUAGES:
            if lang == settings.LANGUAGE_CODE:
                continue
            expected_obj = batch_translate(lang, obj_to_translate)
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

    def test_handle_translate(self):
        mock_field_value = LocalizedValue()
        mock_field_value.set("en", "Hello, World!")
        mock_translate = MagicMock(return_value="Translated text")
        self.translate.translate = mock_translate

        self.translate._handle_translate(mock_field_value, "en", "Hello, World!")

        mock_translate.assert_called_once_with("en", "Hello, World!")
        self.assertEqual(mock_field_value.get("en"), "Translated text")

    def test_batch_process_without_force_and_fulfilled(self):
        data = {}
        for lang, _code in settings.LANGUAGES:
            data[lang] = "value"

        self.instance: Post = PostFactory(title=data, description=data, body=data)
        self.translate = BaseTranslate(self.instance)

        self.translate.translate = MagicMock(side_effect=lambda lang, text: text[::-1])
        self.translate.batch_translate = MagicMock(return_value=["Hello, World!"])

        self.translate.can_translate_object = True
        self.translate.process()

        self.translate.batch_translate.assert_not_called()

    def test_batch_process_with_force_and_fulfilled(self):
        data = {}
        for lang, _lang_name in settings.LANGUAGES:
            data[lang] = "value"

        self.instance: Post = PostFactory(title=data, description=data, body=data)
        self.translate = BaseTranslate(self.instance)

        self.translate.translate = MagicMock(side_effect=lambda lang, text: text[::-1])

        def batch_translate(trans_lang, trans_obj):
            return {k: trans_lang + "-" + v for k, v in trans_obj.items()}

        self.translate.batch_translate = MagicMock(side_effect=batch_translate)

        self.translate.can_translate_object = True
        self.translate.process(force=True)
        obj_to_translate = {
            "title": getattr(self.instance.title, settings.LANGUAGE_CODE),
            "description": getattr(self.instance.description, settings.LANGUAGE_CODE),
            "body": getattr(self.instance.body, settings.LANGUAGE_CODE),
        }

        self.translate.batch_translate.assert_has_calls(
            [
                call("ro", obj_to_translate),
                call("vi", obj_to_translate),
            ],
            True,
        )

        self.instance.refresh_from_db()
        for lang, _lang_name in settings.LANGUAGES:
            if lang == settings.LANGUAGE_CODE:
                continue
            expected_obj = batch_translate(lang, obj_to_translate)
            assert getattr(self.instance.title, lang) == expected_obj["title"]
            assert (
                getattr(self.instance.description, lang) == expected_obj["description"]
            )
            assert getattr(self.instance.body, lang) == expected_obj["body"]

    def test_handle_batch_translate(self):
        data = {settings.LANGUAGE_CODE: "value"}

        self.instance: Post = PostFactory(title=data, description=data, body=data)
        self.translate = BaseTranslate(self.instance)

        def batch_translate(trans_lang, trans_obj):
            return {k: trans_lang + "-" + v for k, v in trans_obj.items()}

        self.translate.batch_translate = MagicMock(side_effect=batch_translate)
        self.translate.can_translate_object = True
        self.translate.process()

        obj_to_translate = {
            "title": getattr(self.instance.title, settings.LANGUAGE_CODE),
            "description": getattr(self.instance.description, settings.LANGUAGE_CODE),
            "body": getattr(self.instance.body, settings.LANGUAGE_CODE),
        }

        self.translate.batch_translate.assert_has_calls(
            [
                call("ro", obj_to_translate),
                call("vi", obj_to_translate),
            ],
            True,
        )
        self.instance.refresh_from_db()
        for lang, _lang_name in settings.LANGUAGES:
            if lang == settings.LANGUAGE_CODE:
                continue
            expected_obj = batch_translate(lang, obj_to_translate)
            assert getattr(self.instance.title, lang) == expected_obj["title"]
            assert (
                getattr(self.instance.description, lang) == expected_obj["description"]
            )
            assert getattr(self.instance.body, lang) == expected_obj["body"]
