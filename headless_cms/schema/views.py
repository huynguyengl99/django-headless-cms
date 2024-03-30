from drf_spectacular.views import SpectacularAPIView

from headless_cms.settings import headless_cms_settings


class CMSSpectacularAPIView(SpectacularAPIView):
    custom_settings = {
        "PREPROCESSING_HOOKS": headless_cms_settings.CMS_DRF_SPECTACULAR_PREPROCESSING_HOOKS,
    }
