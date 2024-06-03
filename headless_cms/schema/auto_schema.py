from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import OpenApiParameter


class CustomAutoSchema(AutoSchema):
    """
    Custom AutoSchema for DRF Spectacular.

    This class extends the default AutoSchema provided by DRF Spectacular to add
    global parameters to the OpenAPI schema. Specifically, it adds an "accept-language"
    header parameter to all endpoints.

    Attributes:
        global_params (list): A list of global OpenAPI parameters to be added to all endpoints.

    Configuration:
        To use this custom schema in Django REST Framework, update your settings:

        .. code-block:: python

            # Rest framework
            REST_FRAMEWORK = {
                "DEFAULT_RENDERER_CLASSES": [
                    "rest_framework.renderers.JSONRenderer",
                ],
                "DEFAULT_SCHEMA_CLASS": "headless_cms.schema.auto_schema.CustomAutoSchema",
            }
    """

    global_params = [
        OpenApiParameter(
            name="accept-language",
            type=str,
            location=OpenApiParameter.HEADER,
            description="Language code parameter.",
        )
    ]

    def get_override_parameters(self):
        """
        Get the override parameters for the schema.

        This method extends the default parameters with the global parameters defined in
        the `global_params` attribute.

        Returns:
            list: A list of OpenAPI parameters.
        """
        params = super().get_override_parameters()
        return params + self.global_params
