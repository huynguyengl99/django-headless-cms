from collections.abc import Iterable
from functools import lru_cache

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import ForeignKey, ManyToManyField
from localized_fields import fields
from rest_framework import serializers
from rest_framework.fields import (
    BooleanField,
    CharField,
    FileField,
    FloatField,
    IntegerField,
    SlugField,
)
from rest_framework.serializers import ModelSerializer

from headless_cms import serializer_fields
from headless_cms.fields import AutoLanguageUrlField, LocalizedMartorField
from headless_cms.models import LocalizedDynamicFileModel, LocalizedPublicationModel
from headless_cms.settings import headless_cms_settings


class LocalizedModelSerializer(ModelSerializer):
    """
    A base serializer for models with localized fields.

    This serializer automatically maps localized fields to their corresponding
    serializer fields in the Django REST Framework, making it easier to work with
    models that have multiple language support.

    Field Mapping:
        - LocalizedField -> CharField
        - LocalizedAutoSlugField -> SlugField
        - LocalizedUniqueSlugField -> SlugField
        - LocalizedFileField -> FileField
        - LocalizedIntegerField -> IntegerField
        - LocalizedFloatField -> FloatField
        - LocalizedBooleanField -> BooleanField
        - AutoLanguageUrlField -> UrlField
        - LocalizedMartorField -> LocalizedMartorFieldSerializer
    """

    serializer_field_mapping = ModelSerializer.serializer_field_mapping.copy()
    serializer_field_mapping[fields.LocalizedField] = CharField
    serializer_field_mapping[fields.LocalizedAutoSlugField] = SlugField
    serializer_field_mapping[fields.LocalizedUniqueSlugField] = SlugField
    serializer_field_mapping[fields.LocalizedFileField] = FileField
    serializer_field_mapping[fields.LocalizedIntegerField] = IntegerField
    serializer_field_mapping[fields.LocalizedFloatField] = FloatField
    serializer_field_mapping[fields.LocalizedBooleanField] = BooleanField
    serializer_field_mapping[AutoLanguageUrlField] = serializer_fields.UrlField
    serializer_field_mapping[LocalizedMartorField] = (
        serializer_fields.LocalizedMartorFieldSerializer
    )

    class Meta:
        model = LocalizedPublicationModel
        abstract = True

    def __new__(cls, *args, **kwargs):
        cls.__doc__ = (
            cls.__doc__ or f"Serializer for {cls.Meta.model._meta.object_name}"
        )
        return super().__new__(cls, *args, **kwargs)

    def to_representation(self, instance):
        data = instance.published_data

        if not data:
            return None

        field_list = instance._meta.get_fields()

        rel_fields = {
            field.attname
            for field in field_list
            if field.is_relation and not field.auto_created and field.related_model
        }

        for k, v in data.items():
            if k in rel_fields:
                continue
            setattr(instance, k, v)

        return super().to_representation(instance)

    def __init__(self, *args, **kwargs):
        if not hasattr(self.Meta, "fields"):
            exclude = set()
            if hasattr(self.Meta, "exclude"):
                exclude = set(self.Meta.exclude)
            exclude.update({"published_version"})

            if hasattr(self.Meta, "extra_exclude"):
                field_names = {f.name for f in self.Meta.model._meta.get_fields()}
                exclude.update(set(self.Meta.extra_exclude) & field_names)

            self.Meta.exclude = list(exclude)
        super().__init__(*args, **kwargs)


class LocalizedBaseSerializer(LocalizedModelSerializer):
    """
    A base serializer for localized models.

    This serializer is designed to exclude certain fields by default, making it easier
    to work with models that have localized fields. The excluded fields often include
    those that are not necessary for the serialization process or that require special
    handling.

    Excluded Fields:
        - `position`: Typically used for ordering and not needed in the serialized output.
        - `content_type`: Used by Django's content types framework, often unnecessary in the output.
        - `object_id`: The ID of the related object, usually not needed in the serialized form.

    This list of excluded fields can be extended by modifying the `extra_exclude` attribute
    in the `Meta` class.
    """

    class Meta:
        extra_exclude = [
            "position",
            "content_type",
            "object_id",
            "skip_translation",
        ] + headless_cms_settings.GLOBAL_EXCLUDED_SERIALIZED_FIELDS
        abstract = True


class LocalizedDynamicFileSerializer(LocalizedBaseSerializer):
    """
    A serializer for models with dynamic file fields, primarily used for LocalizedDynamicFileModel.

    This serializer is designed to handle models that have dynamic file fields, such as
    fields for uploaded files or URLs to external resources. It adds a `src` field that
    returns the absolute URL of the file, either from a local source or an external URL.
    """

    src = serializers.SerializerMethodField(required=False, allow_null=True)

    def get_src(self, obj):
        """
        Get the source URL of the file.

        Args:
            obj (models.Model): The model instance.

        Returns:
            str: The source URL.
        """
        src_file = obj.src_file.translate()
        if src_file:
            return self.context["request"].build_absolute_uri(src_file.url)
        elif obj.src_url:
            return obj.src_url.translate()

    class Meta:
        abstract = True
        extra_exclude = LocalizedBaseSerializer.Meta.extra_exclude + [
            "src_url",
            "src_file",
        ]


class HashModelSerializer(serializers.Serializer):
    """
    A serializer for representing a model's data with an additional hash field that reflects
    the recursive hash of the model instance and its related entities.
    """

    id = serializers.IntegerField(read_only=True)
    hash = serializers.SerializerMethodField()

    def get_hash(self, obj) -> str:
        return obj.get_recursive_hash()


def _auto_serializer(
    model: type[models.Model],
    ancestors: Iterable | None = None,
    override_model_serializer_fields: dict | None = None,
) -> type[serializers.ModelSerializer]:
    """
    Helper function to recursively create a serializer for a given model, incorporating handling
    of related fields, custom field serialization logic, and a 'hash' field that dynamically computes
    a hash of the object and its descendants.

    This function is used internally by the `auto_serializer` function. It manages recursion and
    tracks ancestors to avoid infinite recursion in self-referential models. The 'hash' field is
    added at the root level of the serializer, providing a hash that encapsulates the state of the
    object and all its recursively related entities.

    Args:
        model (type[models.Model]): The model class from which the serializer is generated.
        ancestors (Optional[Iterable], optional): A set of ancestor models that are currently
            being processed in the recursion chain to prevent infinite loops. Defaults to None.
        override_model_serializer fields (Optional[dict], optional): A mapping from model classes
            to dictionaries that specify how to override fields in the serializer. Defaults to None.

    Returns:
        type[serializers.ModelSerializer]: A dynamically created serializer class for the specified
        model. This serializer includes handling for related fields, any specific overrides, and a
        'hash' field that represents the composite state of the object and its children.
    """
    entry_point = False
    if ancestors is None:
        entry_point = True
        ancestors = set()
    if override_model_serializer_fields is None:
        override_model_serializer_fields = {}
    ancestors = set(ancestors)

    model_fields = model._meta.get_fields()

    custom_fields = {}

    if model not in ancestors:
        ancestors.add(model)
        for field in model_fields:
            if isinstance(field, ForeignKey) and issubclass(
                field.related_model, LocalizedPublicationModel
            ):
                serializer = _auto_serializer(
                    field.related_model, ancestors, override_model_serializer_fields
                )
                custom_fields.update(
                    {
                        field.name: serializer(
                            allow_null=True, required=False, read_only=True
                        )
                    }
                )
            elif isinstance(field, ManyToManyField) and field.related_model == model:

                def get_objs(self, obj, my_field=field):
                    return self.__class__(
                        getattr(obj, my_field.name).all(), many=True
                    ).data

                custom_fields.update({f"get_{field.name}": get_objs})
            elif (isinstance(field, GenericRelation | ManyToManyField)) and issubclass(
                field.related_model, LocalizedPublicationModel
            ):
                serializer = _auto_serializer(
                    field.related_model, ancestors, override_model_serializer_fields
                )
                custom_fields.update(
                    {
                        field.name: serializer(
                            many=True, required=False, allow_null=True, read_only=True
                        )
                    }
                )

    if override_model_serializer_fields.get(model):
        custom_fields.update(override_model_serializer_fields[model])

    if issubclass(model, LocalizedDynamicFileModel):
        base_serializer = LocalizedDynamicFileSerializer
    else:
        base_serializer = LocalizedBaseSerializer

    if entry_point:
        custom_fields.update(
            {
                "hash": serializers.SerializerMethodField(
                    required=False, allow_null=True, read_only=True
                )
            }
        )

        def get_hash(self, obj) -> str:
            return obj.get_recursive_hash()

        custom_fields.update({"get_hash": get_hash})

    meta_class = type("Meta", (base_serializer.Meta,), {})
    meta_class.model = model
    result = type(
        model.__name__ + "Serializer", (base_serializer,), dict(custom_fields)
    )
    result.Meta = meta_class

    return result


@lru_cache(maxsize=0)
def auto_serializer(
    model: type[models.Model],
    override_model_serializer_fields: dict | None = None,
) -> type[serializers.ModelSerializer]:
    """
    Automatically create a serializer for a given model using Django REST Framework, including
    a 'hash' field that dynamically computes a hash representing the state of the object and its
    descendants.

    This function simplifies the creation of serializers for models with complex relationships or
    custom serialization requirements. It dynamically generates serializers that handle related
    objects and apply specified field overrides. The 'hash' field is included to provide a dynamic
    representation of the state of the object and all its related entities.

    Args:
        model (type[models.Model]): The Django model class for which to create the serializer.
        override_model_serializer_fields (Optional[dict], optional): A dictionary specifying
            custom field serializers, allowing for customization of the generated serializers.
            Defaults to None.

    Returns:
        type[serializers.ModelSerializer]: A dynamically generated serializer class tailored to
        the specified model, capable of handling nested serialization, field overrides, and
        providing a dynamic hash of the object and its descendants.

    """
    return _auto_serializer(
        model, override_model_serializer_fields=override_model_serializer_fields
    )
