from headless_cms.contrib.astrowind.astrowind_posts.models import AWPost, AWPostMetadata
from headless_cms.contrib.astrowind.shared.serializers import AWBaseSerializer


class AWPostMetadataSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWPostMetadata


class AWPostSerializer(AWBaseSerializer):
    metadata = AWPostMetadataSerializer(read_only=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWPost
