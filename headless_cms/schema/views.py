from drf_spectacular.views import SpectacularAPIView

from headless_cms.settings import headless_cms_settings


class CMSSpectacularAPIView(SpectacularAPIView):
    """
    Custom Spectacular API view for CMS.

    This view extends the default Spectacular API view to use custom settings
    for preprocessing hooks, as defined in the headless CMS settings.

    Attributes:
        custom_settings (dict): A dictionary of custom settings for the Spectacular API view.
    """

    custom_settings = {
        "PREPROCESSING_HOOKS": (
            headless_cms_settings.CMS_DRF_SPECTACULAR_PREPROCESSING_HOOKS
        ),
    }
