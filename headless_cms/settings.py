from typing import Any

from django.conf import settings
from rest_framework.settings import APISettings

HEADLESS_CMS_DEFAULTS: dict[str, Any] = {
    "AUTO_TRANSLATE_CLASS": "headless_cms.auto_translate.BaseTranslate",
    "CMS_DRF_SPECTACULAR_PREPROCESSING_HOOKS": [
        "headless_cms.schema.preprocessing_hooks.preprocessing_filter_spec"
    ],
    "AUTO_TRANSLATE_IGNORES": [],
    "GLOBAL_EXCLUDED_SERIALIZED_FIELDS": [],
    "OPENAI_CHAT_MODEL": "gpt-4-turbo",
    "OPENAI_CLIENT": "openai.OpenAI",
    "DEFAULT_CMS_PERMISSION_CLASS": "rest_framework.permissions.AllowAny",
    "CMS_HOST": "http://localhost:8000",
}

IMPORT_STRINGS = [
    "AUTO_TRANSLATE_CLASS",
    "OPENAI_CLIENT",
    "DEFAULT_CMS_PERMISSION_CLASS",
]


class HeadlessCMSSettings(APISettings):
    _original_settings: dict[str, Any] = {}


headless_cms_settings = HeadlessCMSSettings(
    user_settings=getattr(settings, "HEADLESS_CMS_SETTINGS", {}),  # type: ignore
    defaults=HEADLESS_CMS_DEFAULTS,  # type: ignore
    import_strings=IMPORT_STRINGS,
)
