from headless_cms.contrib.astrowind.astrowind_pages.models import AWIndexPage
from headless_cms.contrib.astrowind.astrowind_widgets.serializers import (
    AWCallToActionSerializer,
    AWFaqSerializer,
    AWFeatureSerializer,
    AWHeroSerializer,
    AWStepSerializer,
)
from headless_cms.serializers import LocalizedModelSerializer


class AWBaseSerializer(LocalizedModelSerializer):
    class Meta:
        extra_exclude = ["id", "position", "content_type", "object_id"]
        abstract = True


class AWIndexPageSerializer(AWBaseSerializer):
    hero = AWHeroSerializer(read_only=True)
    features = AWFeatureSerializer(read_only=True)
    steps = AWStepSerializer(read_only=True)
    faqs = AWFaqSerializer(read_only=True)
    cta = AWCallToActionSerializer(read_only=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWIndexPage
