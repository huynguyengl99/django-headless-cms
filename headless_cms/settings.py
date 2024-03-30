from contextlib import contextmanager
from typing import Any

from django.conf import settings
from rest_framework.settings import APISettings, perform_import

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

    def apply_patches(self, patches):
        for attr, val in patches.items():
            if attr in self.import_strings:
                val = perform_import(val, attr)  # noqa
            # load and store original value, then override __dict__ entry
            self._original_settings[attr] = getattr(self, attr)
            setattr(self, attr, val)

    def clear_patches(self):
        for attr, orig_val in self._original_settings.items():
            setattr(self, attr, orig_val)
        self._original_settings = {}


headless_cms_settings = HeadlessCMSSettings(
    user_settings=getattr(settings, "HEADLESS_CMS_SETTINGS", {}),  # type: ignore
    defaults=HEADLESS_CMS_DEFAULTS,  # type: ignore
    import_strings=IMPORT_STRINGS,
)


@contextmanager
def patched_settings(patches):
    """temporarily patch the global spectacular settings (or do nothing)"""
    if not patches:
        yield
    else:
        try:
            headless_cms_settings.apply_patches(patches)
            yield
        finally:
            headless_cms_settings.clear_patches()
