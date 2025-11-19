from django.conf import settings
from localized_fields.fields import LocalizedField
from localized_fields.fields.file_field import LocalizedFileField
from localized_fields.models import LocalizedModel
from localized_fields.value import LocalizedValue

from headless_cms.fields import LocalizedUrlField


class BaseTranslate:
    """
    Base class for translating localized fields in Django models.

    This class provides the framework for translating localized fields in Django models,
    specifically for use with translation buttons in the Django admin interface.

    Attributes:
        can_batch_translate (bool): Indicates whether the class supports batch translation.

    Args:
        instance (LocalizedModel): The Django model instance to be translated.
    """

    can_batch_translate = False

    def __init__(self, instance: LocalizedModel):
        self.instance = instance
        self.fields = instance._meta.get_fields()

    def translate(self, language: str, text: str):
        """
        Translate text to a single language.

        This method should be overridden in subclasses to provide the actual translation logic.

        Args:
            language (str): The target language code.
            text (str): The text to be translated.

        Returns:
            str: The translated text.
        """
        return text

    def batch_translate(self, batches: dict[str, dict]) -> dict[str, dict]:
        """
        Batch translate multiple fields to a single language.

        This method should be overridden in subclasses to provide the actual batch translation logic.

        Args:
            batches (dict[str, dict]): A dictionary where keys are language codes and values
                are dictionaries mapping field names to text to be translated.

        Returns:
            dict[str, dict]: A dictionary where keys are language codes and values are
                dictionaries mapping field names to translated text.
        """
        raise NotImplementedError

    def _handle_translate(self, field_value: LocalizedValue, lang: str, text: str):
        translated_value = self.translate(lang, text)
        field_value.set(lang, translated_value)

    def _prepare_batch_translate(
        self, force: bool
    ) -> tuple[dict[str, dict], dict[str, dict]]:
        batches = {}
        clean_batches = {}

        for lang, _lang_name in settings.LANGUAGES:
            if lang == settings.LANGUAGE_CODE:
                continue
            obj_to_translate = {}
            obj_to_clean = {}

            for field in self.fields:
                if isinstance(field, LocalizedField) and not isinstance(
                    field, LocalizedFileField | LocalizedUrlField
                ):
                    field_value = getattr(self.instance, field.name)
                    base_value = getattr(field_value, settings.LANGUAGE_CODE)
                    if base_value:
                        if not force and getattr(field_value, lang):
                            continue

                        obj_to_translate[field.name] = base_value
                    else:
                        obj_to_clean[field.name] = ""

            if obj_to_translate or force:
                batches[lang] = obj_to_translate
            if obj_to_clean:
                clean_batches[lang] = obj_to_clean

        return batches, clean_batches

    def _handle_batch_translate(self, force: bool):
        fields_map = {
            field.name: getattr(self.instance, field.name)
            for field in self.fields
            if isinstance(field, LocalizedField)
        }

        batches, clean_batches = self._prepare_batch_translate(force)

        translated_batches = self.batch_translate(batches)

        for lang, translated_obj in translated_batches.items():
            for k, v in translated_obj.items():
                fields_map[k].set(lang, v or "")

        for lang, obj in clean_batches.items():
            for k, v in obj.items():
                fields_map[k].set(lang, v)

        for k, v in fields_map.items():
            setattr(self.instance, k, v)

    def _process_translation(self, force):
        if self.can_batch_translate:
            self._handle_batch_translate(force)
        else:
            for lang, _lang_name in settings.LANGUAGES:
                if lang == settings.LANGUAGE_CODE:
                    continue

                else:
                    for field in self.fields:
                        if isinstance(field, LocalizedField) and not isinstance(
                            field, LocalizedFileField | LocalizedUrlField
                        ):
                            field_value = getattr(self.instance, field.name)
                            base_value = getattr(field_value, settings.LANGUAGE_CODE)
                            if base_value:
                                if not force and getattr(field_value, lang):
                                    continue

                                self._handle_translate(field_value, lang, base_value)
                            elif force:
                                setattr(self.instance, field.name, {})

        self.instance.save()

    def process(self, force=False):
        """
        Process the translation for the database object instance.

        This method translates all localized fields of the instance.

        Args:
            force (bool): Whether to force retranslation for all localized fields
                (even if the fields are already translated).
        """
        self._process_translation(force)
