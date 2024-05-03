from headless_cms.mixins import CMSSchemaMixin
from headless_cms.serializers import auto_serializer
from rest_framework import viewsets

from test_app.models import Post


class PostCMSViewSet(CMSSchemaMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Post.published_objects.published()
    serializer_class = auto_serializer(Post)
