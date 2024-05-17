from django.conf import settings
from localized_fields.fields import LocalizedField
from localized_fields.fields.file_field import LocalizedFileField
from localized_fields.models import LocalizedModel
from localized_fields.value import LocalizedValue


class BaseTranslate:
    """Class to use when click on admin translation buttons.

    Attributes:
        can_translate_object: Indicates whether the inherited class can translate multiple fields
         in batch or not for improving the processing time.
    """

    can_batch_translate = False

    def __init__(self, instance: LocalizedModel):
        self.instance = instance
        self.fields = instance._meta.get_fields()

    def translate(self, language: str, text: str):
        """Override this function to translate text to a single language"""
        return text

    def batch_translate(self, batches: dict[str, dict]) -> dict[str, dict]:
        """Override this function to translate an object to a single language"""
        raise NotImplementedError

    def _handle_translate(self, field_value: LocalizedValue, lang: str, text: str):
        translated_value = self.translate(lang, text)
        field_value.set(lang, translated_value)

    def _prepare_batch_translate(self, force: bool) -> dict[str, dict]:
        batches = {}

        for lang, _lang_name in settings.LANGUAGES:
            if lang == settings.LANGUAGE_CODE:
                continue
            obj_to_translate = {}

            for field in self.fields:
                if isinstance(field, LocalizedField) and not isinstance(
                    field, LocalizedFileField
                ):
                    field_value = getattr(self.instance, field.name)
                    base_value = getattr(field_value, settings.LANGUAGE_CODE)
                    if base_value:
                        if not force and getattr(field_value, lang):
                            continue

                        obj_to_translate[field.name] = base_value

            if obj_to_translate or force:
                batches[lang] = obj_to_translate

        return batches

    def _handle_batch_translate(self, force: bool):
        fields_map = {
            field.name: getattr(self.instance, field.name)
            for field in self.fields
            if isinstance(field, LocalizedField)
        }

        batches = self._prepare_batch_translate(force)

        translated_batches = self.batch_translate(batches)

        for lang, translated_obj in translated_batches.items():
            for k, v in translated_obj.items():
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
                            field, LocalizedFileField
                        ):
                            field_value = getattr(self.instance, field.name)
                            base_value = getattr(field_value, settings.LANGUAGE_CODE)
                            if base_value:
                                if not force and getattr(field_value, lang):
                                    continue

                                self._handle_translate(field_value, lang, base_value)

        self.instance.save()

    def process(self, force=False):
        """Call this one to process the translation for the database object instance, it will translate
        all localized fields.

        Arguments:
            force: whether to force retranslation for all localized fields(even
                the fields are already translated).
        """
        self._process_translation(force)
