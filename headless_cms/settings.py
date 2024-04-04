from typing import Any

from django.conf import settings
from rest_framework.settings import APISettings

HEADLESS_CMS_DEFAULTS: dict[str, Any] = {
    "AUTO_TRANSLATE_CLASS": "headless_cms.auto_translate.BaseTranslate",
    "CMS_DRF_SPECTACULAR_PREPROCESSING_HOOKS": [
        "headless_cms.schema.preprocessing_hooks.preprocessing_filter_spec"
    ],
}

IMPORT_STRINGS = [
    "AUTO_TRANSLATE_CLASS",
]


class HeadlessCMSSettings(APISettings):
    _original_settings: dict[str, Any] = {}


headless_cms_settings = HeadlessCMSSettings(
    user_settings=getattr(settings, "HEADLESS_CMS_SETTINGS", {}),  # type: ignore
    defaults=HEADLESS_CMS_DEFAULTS,  # type: ignore
    import_strings=IMPORT_STRINGS,
)
