from django.http import Http404
from rest_framework.generics import RetrieveAPIView

from headless_cms.contrib.astrowind.astrowind_pages.models import (
    AWAboutPage,
    AWContactPage,
    AWIndexPage,
    AWPostPage,
    AWPricingPage,
    AWSite,
)
from headless_cms.mixins import CMSSchemaMixin
from headless_cms.serializers import auto_serializer


class AWPageView(CMSSchemaMixin, RetrieveAPIView):
    model = None

    def get_object(self):
        obj = self.model.published_objects.published(auto_prefetch=True).first()
        if not obj:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj


class AWIndexPageView(AWPageView):
    serializer_class = auto_serializer(AWIndexPage)
    model = AWIndexPage


class AWSiteView(AWPageView):
    serializer_class = auto_serializer(AWSite)
    model = AWSite


class AWAboutPageView(AWPageView):
    serializer_class = auto_serializer(AWAboutPage)
    model = AWAboutPage


class AWPricingPageView(AWPageView):
    serializer_class = auto_serializer(AWPricingPage)
    model = AWPricingPage


class AWContactPageView(AWPageView):
    serializer_class = auto_serializer(AWContactPage)
    model = AWContactPage


class AWPostPageView(AWPageView):
    serializer_class = auto_serializer(AWPostPage)
    model = AWPostPage
