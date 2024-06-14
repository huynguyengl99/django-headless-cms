from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.settings import api_settings as rest_framework_settings

from headless_cms.serializers import HashModelSerializer
from headless_cms.settings import headless_cms_settings


class CMSSchemaMixin:
    """
    Mixin to include views in the OpenAPI schema documentation for the CMS.

    This mixin is used to dynamically generate documentation for the OpenAPI schema,
    ensuring that only views extending this mixin will be included in the generated
    schema. It also provides default CMS permission classes for Django REST Framework
    views.

    Attributes:
        permission_classes (list): A list of permission classes that includes the default
            CMS permission class followed by the default permission classes from Django
            REST Framework settings.

    Example:
        This mixin can be used in a Django REST Framework view to include the view in
        the OpenAPI schema documentation and enforce CMS-specific permission policies.

        .. code-block:: python

            from rest_framework.views import APIView
            from headless_cms.mixins import CMSSchemaMixin

            class MyCMSView(CMSSchemaMixin, APIView):
                # Your view implementation here
                pass
    """

    permission_classes = [
        headless_cms_settings.DEFAULT_CMS_PERMISSION_CLASS
    ] + rest_framework_settings.DEFAULT_PERMISSION_CLASSES

    def __init_subclass__(cls, **kwargs):
        cls.__doc__ = cls.__doc__ or " "


class HashModelMixin:
    """
    A mixin that adds hash-related actions to a Django REST Framework viewset.

    This mixin provides actions to retrieve hash data for a list of model instances.
    """

    @extend_schema(
        responses=HashModelSerializer(many=True),
    )
    @action(
        detail=False,
        methods=["GET"],
        pagination_class=None,
        serializer_class=HashModelSerializer,
    )
    def hash(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = HashModelSerializer(queryset, many=True)
        return Response(serializer.data)
