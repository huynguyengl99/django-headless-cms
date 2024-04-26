from rest_framework.relations import RelatedField

from headless_cms.contrib.astrowind.astrowind_posts.models import (
    AWCategory,
    AWPost,
    AWPostMetadata,
    AWPostTag,
)
from headless_cms.contrib.astrowind.shared.serializers import AWBaseSerializer


class AWPostMetadataSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWPostMetadata


class AWPostTagSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWPostTag


class AWPostImageSerializer(RelatedField):
    class Meta(AWBaseSerializer.Meta):
        model = AWPostTag

    def to_representation(self, obj):
        if obj.src:
            return self.context["request"].build_absolute_uri(obj.src.url)
        elif obj.src_url:
            return obj.src_url


class AWCategorySerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWCategory


class AWPostSerializer(AWBaseSerializer):
    metadata = AWPostMetadataSerializer(read_only=True)
    category = AWCategorySerializer(read_only=True)
    image = AWPostImageSerializer(read_only=True)

    tags = AWPostTagSerializer(many=True, read_only=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWPost
