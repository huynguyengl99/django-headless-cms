from headless_cms.contrib.astrowind.astrowind_posts.models import AWPost
from headless_cms.contrib.astrowind.astrowind_widgets.models import AWImage
from headless_cms.serializers import (
    LocalizedBaseSerializer,
    LocalizedDynamicFileSerializer,
)


class RelatedPostImageSerializer(LocalizedDynamicFileSerializer):
    class Meta(LocalizedDynamicFileSerializer.Meta):
        model = AWImage


class RelatedPostSerializer(LocalizedBaseSerializer):
    image = RelatedPostImageSerializer()

    class Meta(LocalizedBaseSerializer.Meta):
        model = AWPost
        fields = ["id", "title", "excerpt", "author", "slug", "image"]
