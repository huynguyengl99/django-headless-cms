from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import ForeignKey
from localized_fields import fields
from rest_framework.fields import (
    BooleanField,
    CharField,
    FileField,
    FloatField,
    IntegerField,
    SlugField,
)
from rest_framework.serializers import ModelSerializer

from .models import PublicationModel


class LocalizedModelSerializer(ModelSerializer):
    serializer_field_mapping = ModelSerializer.serializer_field_mapping.copy()
    serializer_field_mapping[fields.LocalizedField] = CharField
    serializer_field_mapping[fields.LocalizedAutoSlugField] = SlugField
    serializer_field_mapping[fields.LocalizedUniqueSlugField] = SlugField
    serializer_field_mapping[fields.LocalizedFileField] = FileField
    serializer_field_mapping[fields.LocalizedIntegerField] = IntegerField
    serializer_field_mapping[fields.LocalizedFloatField] = FloatField
    serializer_field_mapping[fields.LocalizedBooleanField] = BooleanField

    def to_representation(self, instance):
        data = instance.published_data

        if not data:
            return None

        field_list = instance._meta.get_fields()
        fk_fields = {
            field.attname: field
            for field in field_list
            if isinstance(field, ForeignKey)
            and field.attname in data
            and field.name != "content_type"
        }
        related_fields = []

        for f in field_list:
            if f.auto_created and not f.concrete:
                related_fields.append(f.related_name)
            elif isinstance(f, GenericRelation) and f.name != "versions":
                related_fields.append(f.name)

        data.update(
            {field: getattr(instance, field).all() for field in related_fields if field}
        )

        for field_id_name, field in fk_fields.items():
            field_id = data[field_id_name]
            if not field_id:
                data.update({field_id_name: field_id})
                continue

            rel_model = field.related_model
            if not isinstance(rel_model, PublicationModel):
                rel_instance = getattr(instance, field.name)
            else:
                rel_instance = (
                    rel_model.published_objects.published().filter(id=field_id).first()
                )
            data[field.name] = rel_instance

        return super().to_representation(data)

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
