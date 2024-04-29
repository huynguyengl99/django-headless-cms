import reversion
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from localized_fields.fields import LocalizedField
from localized_fields.models import LocalizedModel
from localized_fields.value import LocalizedValue


class BaseTranslate:
    """Class to use when click on admin translation buttons.

    Attributes:
        can_translate_object: Indicates whether the inherited class can translate multiple fields
         in batch or not for improving the processing time.
    """

    can_translate_object = False

    def __init__(self, instance: LocalizedModel, user=None):
        self.instance = instance
        self.fields = instance._meta.get_fields()
        self.user = user

    def translate(self, language: str, text: str):
        """Override this function to translate text to a single language"""
        return text

    def batch_translate(self, language: str, obj_to_translate: dict):
        """Override this function to translate an object to a single language"""
        raise NotImplementedError

    def _handle_translate(self, field_value: LocalizedValue, lang: str, text: str):
        translated_value = self.translate(lang, text)
        field_value.set(lang, translated_value)

    def _handle_batch_translate(self, lang: str, force: bool):
        obj_to_translate = {}
        fields_map = {}
        for field in self.fields:
            if isinstance(field, LocalizedField):
                field_value = getattr(self.instance, field.name)
                base_value = getattr(field_value, settings.LANGUAGE_CODE)
                if base_value:
                    if not force and getattr(field_value, lang):
                        continue

                    obj_to_translate[field.name] = base_value
                    fields_map[field.name] = getattr(self.instance, field.name)

        if not obj_to_translate and not force:
            return

        translated_texts = self.batch_translate(lang, obj_to_translate)
        for k, v in translated_texts.items():
            fields_map[k].set(lang, v)

    def _process_translation(self, force):
        for lang, _lang_name in settings.LANGUAGES:
            if lang == settings.LANGUAGE_CODE:
                continue

            if self.can_translate_object:
                self._handle_batch_translate(lang, force)
            else:
                for field in self.fields:
                    if isinstance(field, LocalizedField):
                        field_value = getattr(self.instance, field.name)
                        base_value = getattr(field_value, settings.LANGUAGE_CODE)
                        if base_value:
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

    def process(self, force=False):
        """Call this one to process the translation for the database object instance, it will translate
        all localized fields.

        Arguments:
            force: whether to force retranslation for all localized fields(even
                the fields are already translated).
        """
        with reversion.create_revision():
            reversion.set_comment(f"Object translated{' (forced)' if force else ''}.")

            if self.user:
                reversion.set_user(self.user)

            self._process_translation(force)
