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
    RelatedPostSerializer,
)
from headless_cms.mixins import CMSSchemaMixin, HashModelMixin
from headless_cms.serializers import auto_serializer


class AWPostPaginator(PageNumberPagination):
    page_size = 10
    page_size_query_param = "size"


class PostFilter(django_filters.FilterSet):
    id = django_filters.AllValuesMultipleFilter()
    category = extend_schema_field(OpenApiTypes.STR)(
        django_filters.AllValuesFilter(
            field_name="category__slug",
            method="filter_slug",
        )
    )
    tag = extend_schema_field(OpenApiTypes.STR)(
        django_filters.AllValuesFilter(
            field_name="tags__slug",
            method="filter_slug",
        )
    )

    def filter_slug(self, queryset, name, value):
        return queryset.filter(Q(**{name + "__iexact": value}))

    class Meta:
        model = AWPost
        fields = ["id", "category", "tag"]


class AWPostCMSViewSet(CMSSchemaMixin, HashModelMixin, ReadOnlyModelViewSet):
    queryset = AWPost.published_objects.published(auto_prefetch=True)
    serializer_class = auto_serializer(
        AWPost,
        override_model_serializer_fields={
            AWPost: {"related_posts": RelatedPostSerializer(read_only=True, many=True)}
        },
    )
    filterset_class = PostFilter
    pagination_class = AWPostPaginator


class AWPostTagViewSet(CMSSchemaMixin, HashModelMixin, ReadOnlyModelViewSet):
    queryset = AWPostTag.published_objects.published()
    serializer_class = auto_serializer(AWPostTag)
    pagination_class = None


class AWCategoryViewSet(CMSSchemaMixin, HashModelMixin, ReadOnlyModelViewSet):
    queryset = AWCategory.published_objects.published()
    serializer_class = auto_serializer(AWCategory)
    pagination_class = None
