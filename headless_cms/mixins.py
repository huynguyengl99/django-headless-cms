from rest_framework.settings import api_settings as rest_framework_settings

from headless_cms.settings import headless_cms_settings


class CMSSchemaMixin:
    permission_classes = [
        headless_cms_settings.DEFAULT_CMS_PERMISSION_CLASS
    ] + rest_framework_settings.DEFAULT_PERMISSION_CLASSES
