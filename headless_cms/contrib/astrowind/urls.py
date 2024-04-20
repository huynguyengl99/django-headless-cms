from django.urls import include, path

from headless_cms.contrib.astrowind.astrowind_pages.views import (
    AWAboutPageView,
    AWIndexPageView,
    AWPricingPageView,
    AWSiteView,
)

urlpatterns = [
    path("index", AWIndexPageView.as_view(), name="index"),
    path("about", AWAboutPageView.as_view(), name="about"),
    path("site", AWSiteView.as_view(), name="site"),
    path("pricing", AWPricingPageView.as_view(), name="pricing"),
    path(
        "posts",
        include(("headless_cms.contrib.astrowind.astrowind_posts.urls", "posts")),
    ),
]
