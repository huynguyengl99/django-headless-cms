from django.urls import path
from drf_spectacular.settings import spectacular_settings
from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView

from .views import CMSSpectacularAPIView


class CustomSpectacularSwaggerView(SpectacularSwaggerView):
    def _get_schema_auth_names(self):
        return super()._get_schema_auth_names() + [
            list(auth.keys())[0] for auth in spectacular_settings.SECURITY
        ]


urlpatterns = [
    path("api/cms-schema/", CMSSpectacularAPIView.as_view(), name="cms-schema"),
    path(
        "api/cms-schema/swg/",
        CustomSpectacularSwaggerView.as_view(url_name="cms-schema"),
        name="cms-swagger-ui",
    ),
    path(
        "api/cms-schema/redoc/",
        SpectacularRedocView.as_view(url_name="cms-schema"),
        name="cms-redoc",
    ),
]
