from django.urls import path
from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView

from .views import CMSSpectacularAPIView

urlpatterns = [
    path("api/cms-schema/", CMSSpectacularAPIView.as_view(), name="cms-schema"),
    path(
        "api/cms-schema/swg/",
        SpectacularSwaggerView.as_view(url_name="cms-schema"),
        name="cms-swagger-ui",
    ),
    path(
        "api/cms-schema/redoc/",
        SpectacularRedocView.as_view(url_name="cms-schema"),
        name="cms-redoc",
    ),
]
