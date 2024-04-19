from rest_framework.viewsets import ReadOnlyModelViewSet

from headless_cms.contrib.astrowind.astrowind_posts.models import AWPost
from headless_cms.contrib.astrowind.astrowind_posts.serializers import AWPostSerializer
from headless_cms.mixins import CMSSchemaMixin


class AWPostCMSViewSet(CMSSchemaMixin, ReadOnlyModelViewSet):
    queryset = AWPost.published_objects.published(auto_prefetch=True)
    serializer_class = AWPostSerializer
