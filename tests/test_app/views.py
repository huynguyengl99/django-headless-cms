from rest_framework import viewsets

from test_app.models import Post
from test_app.serializers import PostSerializer


class PostCMSViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.published_objects.published()
    serializer_class = PostSerializer
