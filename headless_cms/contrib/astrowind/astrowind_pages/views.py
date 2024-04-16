from django.http import Http404
from rest_framework.generics import RetrieveAPIView

from headless_cms.contrib.astrowind.astrowind_pages.models import AWIndexPage, AWSite
from headless_cms.contrib.astrowind.astrowind_pages.serializers import (
    AWIndexPageSerializer,
    AWSiteSerializer,
)


class AWIndexPageCMSView(RetrieveAPIView):
    serializer_class = AWIndexPageSerializer

    def get_object(self):
        obj = AWIndexPage.published_objects.published(auto_prefetch=True).first()
        if not obj:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj


class AWSiteCMSView(RetrieveAPIView):
    serializer_class = AWSiteSerializer

    def get_object(self):
        obj = AWSite.published_objects.published(auto_prefetch=True).first()
        if not obj:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj
