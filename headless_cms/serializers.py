from collections.abc import Iterable
from functools import lru_cache
from typing import Optional

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
from headless_cms.fields.martor_field import LocalizedMartorField
from headless_cms.fields.url_field import AutoLanguageUrlField
from headless_cms.models import LocalizedDynamicFileModel, LocalizedPublicationModel
from headless_cms.settings import headless_cms_settings


class LocalizedModelSerializer(ModelSerializer):
    serializer_field_mapping = ModelSerializer.serializer_field_mapping.copy()
    serializer_field_mapping[fields.LocalizedField] = CharField
    serializer_field_mapping[fields.LocalizedAutoSlugField] = SlugField
    serializer_field_mapping[fields.LocalizedUniqueSlugField] = SlugField
    serializer_field_mapping[fields.LocalizedFileField] = FileField
    serializer_field_mapping[fields.LocalizedIntegerField] = IntegerField
    serializer_field_mapping[fields.LocalizedFloatField] = FloatField
    serializer_field_mapping[fields.LocalizedBooleanField] = BooleanField
    serializer_field_mapping[fields.LocalizedBooleanField] = BooleanField
    serializer_field_mapping[AutoLanguageUrlField] = serializer_fields.UrlField
    serializer_field_mapping[LocalizedMartorField] = (
        serializer_fields.LocalizedMartorField
    )

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
    class Meta:
        extra_exclude = [
            "position",
            "content_type",
            "object_id",
        ] + headless_cms_settings.GLOBAL_EXCLUDED_SERIALIZED_FIELDS
        abstract = True


class LocalizedDynamicFileSerializer(LocalizedBaseSerializer):
    src = serializers.SerializerMethodField()

    def get_src(self, obj):
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


@lru_cache(maxsize=0)
def auto_serializer(  # noqa: C901
    model: type[models.Model],
    ancestors: Optional[Iterable] = None,
    override_model_serializer_fields: Optional[dict] = None,
) -> type[serializers.ModelSerializer]:
    if ancestors is None:
        ancestors = set()
    if override_model_serializer_fields is None:
        override_model_serializer_fields = {}
    ancestors = set(ancestors)

    model_fields = model._meta.get_fields()

    relations = {}

    if model not in ancestors:
        ancestors.add(model)
        for field in model_fields:
            if isinstance(field, ForeignKey) and issubclass(
                field.related_model, LocalizedPublicationModel
            ):
                serializer = auto_serializer(
                    field.related_model, ancestors, override_model_serializer_fields
                )
                relations.update({field.name: serializer(read_only=True)})
            elif isinstance(field, ManyToManyField) and field.related_model == model:

                def get_objs(self, obj, my_field=field):
                    return self.__class__(
                        getattr(obj, my_field.name).all(), many=True
                    ).data

                relations.update({f"get_{field.name}": get_objs})
            elif (isinstance(field, (GenericRelation, ManyToManyField))) and issubclass(
                field.related_model, LocalizedPublicationModel
            ):
                serializer = auto_serializer(
                    field.related_model, ancestors, override_model_serializer_fields
                )
                relations.update({field.name: serializer(many=True, read_only=True)})

    if override_model_serializer_fields.get(model):
        relations.update(override_model_serializer_fields[model])

    if issubclass(model, LocalizedDynamicFileModel):
        base_serializer = LocalizedDynamicFileSerializer
    else:
        base_serializer = LocalizedBaseSerializer

    meta_class = type("Meta", (base_serializer.Meta,), {})
    meta_class.model = model
    result = type(model.__name__ + "Serializer", (base_serializer,), dict(relations))
    result.Meta = meta_class

    return result
