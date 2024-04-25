import django_filters
from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ReadOnlyModelViewSet

from headless_cms.contrib.astrowind.astrowind_posts.models import (
    AWCategory,
    AWPost,
    AWPostTag,
)
from headless_cms.contrib.astrowind.astrowind_posts.serializers import (
    AWCategorySerializer,
    AWPostSerializer,
    AWPostTagSerializer,
)
from headless_cms.mixins import CMSSchemaMixin


class AWPostPaginator(PageNumberPagination):
    page_size = 10
    page_size_query_param = "size"


class PostFilter(django_filters.FilterSet):
    category = extend_schema_field(OpenApiTypes.STR)(
        django_filters.AllValuesFilter(
            field_name="category__title",
            method="filter_category",
        )
    )
    tag = extend_schema_field(OpenApiTypes.STR)(
        django_filters.AllValuesFilter(
            field_name="tags__value",
            method="filter_tag",
        )
    )

    def filter_category(self, queryset, name, value):
        return queryset.filter(Q(**{name: value}))

    def filter_tag(self, queryset, name, value):
        return queryset.filter(Q(**{name: value}))

    class Meta:
        model = AWPost
        fields = ["category", "tag"]


class AWPostCMSViewSet(CMSSchemaMixin, ReadOnlyModelViewSet):
    queryset = AWPost.published_objects.published(auto_prefetch=True)
    serializer_class = AWPostSerializer
    filterset_class = PostFilter
    pagination_class = AWPostPaginator


class AWPostTagViewSet(CMSSchemaMixin, ReadOnlyModelViewSet):
    queryset = AWPostTag.published_objects.published()
    serializer_class = AWPostTagSerializer
    pagination_class = None


class AWCategoryViewSet(CMSSchemaMixin, ReadOnlyModelViewSet):
    queryset = AWCategory.published_objects.published()
    serializer_class = AWCategorySerializer
    pagination_class = None
