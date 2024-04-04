from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from localized_fields.fields import LocalizedField
from localized_fields.models import LocalizedModel
from localized_fields.value import LocalizedValue


class BaseTranslate:
    """Class to use when click on admin translation buttons.

    Attributes:
        can_batch_translate: Indicates whether the inherited class can translate multiple languages
         in batch or not for improving the processing time.
    """

    can_batch_translate = False

    def __init__(self, instance: LocalizedModel):
        self.instance = instance
        self.fields = instance._meta.get_fields()

    def translate(self, language: str, text: str):
        """Override this function to translate text to a single language"""
        return text

    def batch_translate(self, languages: list[str], text: str):
        """Override this function to translate text into multiple languages"""
        raise NotImplementedError

    def _handle_translate(self, field_value: LocalizedValue, lang: str, text: str):
        translated_value = self.translate(lang, text)
        field_value.set(lang, translated_value)

    def _handle_batch_translate(
        self, field_value: LocalizedValue, text: str, force: bool
    ):
        langs_to_translate = []
        for lang, _lang_name in settings.LANGUAGES:
            if lang == settings.LANGUAGE_CODE:
                continue
            if not force and getattr(field_value, lang):
                continue
            langs_to_translate.append(lang)
        translated_texts = self.batch_translate(langs_to_translate, text)
        if len(translated_texts) != len(langs_to_translate):
            return

        for lang, translated_text in zip(langs_to_translate, translated_texts):
            field_value.set(lang, translated_text)

    def process(self, force=False):
        """Call this one to process the translation for the database object instance, it will translate
        all localized fields and recursive calls this one to the child localized models too.

        Arguments:
            force: whether to force retranslation for all localized fields(even
                the fields are already translated).
        """
        for field in self.fields:
            if isinstance(field, LocalizedField):
                field_value = getattr(self.instance, field.name)
                base_value = getattr(field_value, settings.LANGUAGE_CODE)
                if base_value:
                    if self.can_batch_translate:
                        self._handle_batch_translate(field_value, base_value, force)
                    else:
                        for lang, _lang_name in settings.LANGUAGES:
                            if lang == settings.LANGUAGE_CODE:
                                continue
                            if not force and getattr(field_value, lang):
                                continue

                            self._handle_translate(field_value, lang, base_value)
            elif isinstance(field, GenericRelation) and issubclass(
                field.related_model, LocalizedModel
            ):
                sub_items = getattr(self.instance, field.name).all()
                for item in sub_items:
                    self.__class__(item).process(force)
        self.instance.save()
