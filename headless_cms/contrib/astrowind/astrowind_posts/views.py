from rest_framework.viewsets import ReadOnlyModelViewSet

from headless_cms.contrib.astrowind.astrowind_posts.models import AWPost
from headless_cms.contrib.astrowind.astrowind_posts.serializers import AWPostSerializer


class AWPostCMSViewSet(ReadOnlyModelViewSet):
    queryset = AWPost.published_objects.published(auto_prefetch=True)
    serializer_class = AWPostSerializer
