import contextlib

from django.conf import settings
from django.utils.functional import keep_lazy_text
from django.utils.text import slugify
from localized_fields.fields import LocalizedUniqueSlugField
from unidecode import unidecode


@contextlib.contextmanager
def normalized_slugify():
    from localized_fields.fields import uniqueslug_field

    @keep_lazy_text
    def custom_slugify(value, allow_unicode=False):
        return slugify(unidecode(value), allow_unicode=allow_unicode)

    uniqueslug_field.slugify = custom_slugify
    yield
    uniqueslug_field.slugify = slugify


def _get_lazy_language_codes():
    return (lang_code for lang_code, _ in settings.LANGUAGES)


class LocalizedUniqueNormalizedSlugField(LocalizedUniqueSlugField):
    def pre_save(self, instance, add: bool):
        with normalized_slugify():
            return super().pre_save(instance, add)

    def __init__(self, *args, **kwargs):
        kwargs["uniqueness"] = kwargs.pop("uniqueness", Uniqueness)
        super().__init__(*args, **kwargs)


class LazyUniqueness(type):
    def __iter__(cls):
        return iter(_get_lazy_language_codes())


class Uniqueness(metaclass=LazyUniqueness):
    """
    A proxy class that act as a lazy iterator for current language codes.
    """

    pass
