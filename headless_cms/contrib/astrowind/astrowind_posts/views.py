import django_filters
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ReadOnlyModelViewSet

from headless_cms.contrib.astrowind.astrowind_posts.models import (
    AWCategory,
    AWPost,
    AWPostTag,
)
from headless_cms.contrib.astrowind.astrowind_posts.serializers import AWPostSerializer
from headless_cms.mixins import CMSSchemaMixin


class AWPostPaginator(PageNumberPagination):
    page_size = 10
    page_size_query_param = "size"


class PostFilter(django_filters.FilterSet):
    category = extend_schema_field(OpenApiTypes.STR)(
        django_filters.ModelChoiceFilter(
            field_name="category__title",
            to_field_name="title",
            queryset=AWCategory.published_objects.published(),
        )
    )
    tag = extend_schema_field(OpenApiTypes.STR)(
        django_filters.ModelChoiceFilter(
            field_name="tags__value",
            to_field_name="value",
            queryset=AWPostTag.published_objects.published(),
        )
    )

    class Meta:
        model = AWPost
        fields = ["category", "tag"]


class AWPostCMSViewSet(CMSSchemaMixin, ReadOnlyModelViewSet):
    queryset = AWPost.published_objects.published(auto_prefetch=True)
    serializer_class = AWPostSerializer
    filterset_class = PostFilter
    pagination_class = AWPostPaginator

    def get_queryset(self):
        return AWPost.published_objects.published(auto_prefetch=True)
