from django.urls import include, path

from headless_cms.contrib.astrowind.astrowind_pages.views import (
    AWAboutPageView,
    AWContactPageView,
    AWIndexPageView,
    AWPostPageView,
    AWPricingPageView,
    AWSiteView,
)

urlpatterns = [
    path("index/", AWIndexPageView.as_view(), name="index"),
    path("about/", AWAboutPageView.as_view(), name="about"),
    path("site/", AWSiteView.as_view(), name="site"),
    path("post-page/", AWPostPageView.as_view(), name="post-page"),
    path("pricing/", AWPricingPageView.as_view(), name="pricing"),
    path("contact/", AWContactPageView.as_view(), name="contact"),
    path(
        "posts/",
        include("headless_cms.contrib.astrowind.astrowind_posts.urls"),
    ),
]
