from django.http import Http404
from rest_framework.generics import RetrieveAPIView

from headless_cms.contrib.astrowind.astrowind_pages.models import AWIndexPage
from headless_cms.contrib.astrowind.astrowind_pages.serializers import (
    AWIndexPageSerializer,
)


class AWIndexPageCMSView(RetrieveAPIView):
    serializer_class = AWIndexPageSerializer

    def get_object(self):
        obj = AWIndexPage.published_objects.published(auto_prefetch=True).first()
        if not obj:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj
