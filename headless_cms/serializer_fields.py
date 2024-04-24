from django.conf import settings
from django.utils import translation
from rest_framework.fields import (
    CharField,
)
from rest_framework.relations import SlugRelatedField

LANGUAGE_PREFIXES = tuple(f"/{lang}/" for lang in settings.LANGUAGES)


class UrlField(CharField):
    """This field will automatically add language prefix path for relative url (/about => /en/about)
    but will keep the full url as it is."""

    def to_representation(self, value):
        value: str = super().to_representation(value)
        if not value.startswith("/") or value.startswith(LANGUAGE_PREFIXES):
            return value

        language_code = translation.get_language() or settings.LANGUAGE_CODE

        return f"/{language_code}" + value


class LocalizedSlugRelatedField(SlugRelatedField):
    def to_representation(self, obj):
        res = super().to_representation(obj)
        return str(res)
