from django.urls import include, path

from headless_cms.contrib.astrowind.astrowind_pages.views import (
    AWAboutPageHashView,
    AWAboutPageView,
    AWContactPageHashView,
    AWContactPageView,
    AWIndexPageHashView,
    AWIndexPageView,
    AWPostPageHashView,
    AWPostPageView,
    AWPricingPageHashView,
    AWPricingPageView,
    AWSiteHashView,
    AWSiteView,
)

urlpatterns = [
    path("index/", AWIndexPageView.as_view(), name="index"),
    path("index/hash/", AWIndexPageHashView.as_view(), name="index"),
    path("about/", AWAboutPageView.as_view(), name="about"),
    path("about/hash/", AWAboutPageHashView.as_view(), name="about"),
    path("site/", AWSiteView.as_view(), name="site"),
    path("site/hash/", AWSiteHashView.as_view(), name="site"),
    path("post-page/", AWPostPageView.as_view(), name="post-page"),
    path("post-page/hash/", AWPostPageHashView.as_view(), name="post-page"),
    path("pricing/", AWPricingPageView.as_view(), name="pricing"),
    path("pricing/hash/", AWPricingPageHashView.as_view(), name="pricing"),
    path("contact/", AWContactPageView.as_view(), name="contact"),
    path("contact/hash/", AWContactPageHashView.as_view(), name="contact"),
    path(
        "posts/",
        include("headless_cms.contrib.astrowind.astrowind_posts.urls"),
    ),
]
