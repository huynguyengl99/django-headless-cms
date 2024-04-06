from headless_cms.serializers import LocalizedModelSerializer


class AWBaseSerializer(LocalizedModelSerializer):
    class Meta:
        extra_exclude = ["id", "position", "content_type", "object_id"]
        abstract = True
