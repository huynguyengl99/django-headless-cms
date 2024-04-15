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

from headless_cms.fields.url_field import AutoLanguageUrlField
from headless_cms.serializer_fields import UrlField


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
    serializer_field_mapping[AutoLanguageUrlField] = UrlField

    def to_representation(self, instance):
        data = instance.published_data

        if not data:
            return None

        for k, v in data.items():
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
