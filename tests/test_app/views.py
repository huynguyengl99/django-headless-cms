from headless_cms.mixins import CMSSchemaMixin
from headless_cms.serializers import auto_serializer
from rest_framework import viewsets

from test_app.models import Article, Post


class PostCMSViewSet(CMSSchemaMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Post.published_objects.published(auto_prefetch=True)
    serializer_class = auto_serializer(Post)


class ArticleCMSViewSet(CMSSchemaMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Article.published_objects.published(auto_prefetch=True)
    serializer_class = auto_serializer(Article)
