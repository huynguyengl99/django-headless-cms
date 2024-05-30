from django.conf import settings
from django.utils import translation
from rest_framework.fields import (
    CharField,
)

from headless_cms.utils.markdown import replace_placeholder

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


class LocalizedMartorFieldSerializer(CharField):
    def to_representation(self, value):
        return replace_placeholder(str(value), False)
