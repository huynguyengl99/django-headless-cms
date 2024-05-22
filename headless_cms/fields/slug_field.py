import contextlib

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


class LocalizedUniqueNormalizedSlugField(LocalizedUniqueSlugField):
    def pre_save(self, instance, add: bool):
        with normalized_slugify():
            return super().pre_save(instance, add)
