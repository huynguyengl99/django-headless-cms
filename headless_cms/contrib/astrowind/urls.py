from django.urls import path

from headless_cms.contrib.astrowind.astrowind_pages.views import (
    AWIndexPageCMSView,
    AWSiteCMSView,
)

urlpatterns = [
    path("index", AWIndexPageCMSView.as_view(), name="index"),
    path("site", AWSiteCMSView.as_view(), name="site"),
]
