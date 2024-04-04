from rest_framework.generics import RetrieveAPIView

from headless_cms.contrib.astrowind.astrowind_pages.models import AWIndexPage
from headless_cms.contrib.astrowind.astrowind_pages.serializers import (
    AWIndexPageSerializer,
)


class AWIndexPageCMSView(RetrieveAPIView):
    serializer_class = AWIndexPageSerializer

    def get_object(self):
        obj, created = (
            AWIndexPage.published_objects.select_related(
                "hero__published_version",
                "features__published_version",
                "steps__published_version",
                "steps__image__published_version",
                "faqs__published_version",
                "cta__published_version",
            )
            .prefetch_related(
                "hero__actions__published_version",
                "features__items__published_version",
                "steps__items__published_version",
                "faqs__items__published_version",
                "cta__actions__published_version",
            )
            .get_or_create(pk=AWIndexPage.singleton_instance_id)
        )
        self.check_object_permissions(self.request, obj)
        return obj
