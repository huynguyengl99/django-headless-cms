from unittest.mock import MagicMock

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
        self.translate.translate = MagicMock(side_effect=lambda lang, text: text[::-1])
        self.translate.batch_translate = MagicMock(return_value=["Hello, World!"])

        self.translate.can_batch_translate = True
        self.translate.process()

        self.translate.translate.assert_not_called()
        self.translate.batch_translate.assert_called()

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

        self.translate.can_batch_translate = True
        self.translate.process()

        self.translate.batch_translate.assert_called_with([], "value")

    def test_batch_process_with_force_and_fulfilled(self):
        data = {}
        for lang, _code in settings.LANGUAGES:
            data[lang] = "value"

        self.instance: Post = PostFactory(title=data, description=data, body=data)
        self.translate = BaseTranslate(self.instance)

        self.translate.translate = MagicMock(side_effect=lambda lang, text: text[::-1])
        self.translate.batch_translate = MagicMock(return_value=["Hello, World!"])

        self.translate.can_batch_translate = True
        self.translate.process(force=True)

        self.translate.batch_translate.assert_called_with(["ro", "vi"], "value")

    def test_handle_batch_translate(self):
        langs_to_translate = [
            lang for lang, _ in settings.LANGUAGES if lang != settings.LANGUAGE_CODE
        ]

        mock_field_value = LocalizedValue()
        mock_field_value.set(settings.LANGUAGE_CODE, "Hello, World!")
        mock_batch_translate = MagicMock(
            return_value=["Translated text" for _ in langs_to_translate]
        )
        self.translate.batch_translate = mock_batch_translate

        self.translate._handle_batch_translate(mock_field_value, "Hello, World!", False)

        mock_batch_translate.assert_called_once_with(
            langs_to_translate, "Hello, World!"
        )
        for lang in langs_to_translate:
            self.assertEqual(mock_field_value.get(lang), "Translated text")
