import contextlib

from django.conf import settings
from django.utils.functional import keep_lazy_text
from django.utils.text import slugify
from localized_fields.fields import LocalizedUniqueSlugField
from unidecode import unidecode


@contextlib.contextmanager
def normalized_slugify():
    """
    Context manager to temporarily override the slugify function to use a custom slugify function
    that normalizes the value using unidecode.
    """
    from localized_fields.fields import uniqueslug_field

    @keep_lazy_text
    def custom_slugify(value, allow_unicode=False):
        return slugify(unidecode(value), allow_unicode=allow_unicode)

    uniqueslug_field.slugify = custom_slugify
    yield
    uniqueslug_field.slugify = slugify


def _get_lazy_language_codes():
    """
    Generator function to yield language codes from the settings.LANGUAGES configuration.

    :return: A generator for language codes.
    """
    return (lang_code for lang_code, _ in settings.LANGUAGES)


class LocalizedUniqueNormalizedSlugField(LocalizedUniqueSlugField):
    """
    A custom field that extends LocalizedUniqueSlugField to provide a localized unique slug field
    with normalized slugs for multi-language support.
    """

    def pre_save(self, instance, add: bool):
        """
        Overrides the pre_save method to use the normalized slugify function within the context manager.

        :param instance: The model instance being saved.
        :param add: A boolean indicating whether this is a new instance being added.
        :return: The value to be saved to the database.
        """
        with normalized_slugify():
            return super().pre_save(instance, add)

    def __init__(self, *args, **kwargs):
        """
        Initializes the field with the specified arguments and sets the uniqueness attribute.

        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        """
        kwargs["uniqueness"] = kwargs.pop("uniqueness", Uniqueness)
        super().__init__(*args, **kwargs)


class LazyUniqueness(type):
    """
    Metaclass for Uniqueness that allows it to be an iterable, providing language codes lazily.
    """

    def __iter__(cls):
        return iter(_get_lazy_language_codes())


class Uniqueness(metaclass=LazyUniqueness):
    """
    A proxy class that acts as a lazy iterator for current language codes.
    """

    pass
