import django_filters
from django_filters import rest_framework as filters


class CMSFilterBackend(filters.DjangoFilterBackend):
    """
    A custom filter backend that extends DjangoFilterBackend to provide filtering by multiple IDs when no
    custom filterset class is defined for the view.
    """

    def get_filterset_class(self, view, queryset=None):
        filterset_class = super().get_filterset_class(view, queryset)
        if filterset_class:
            return filterset_class

        from headless_cms.mixins import HashModelMixin

        if not isinstance(view, HashModelMixin):
            return None

        class IdFilter(django_filters.FilterSet):
            id = django_filters.AllValuesMultipleFilter()

        return IdFilter
