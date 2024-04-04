from headless_cms.contrib.astrowind.astrowind_widgets.models import (
    AWAction,
    AWCallToAction,
    AWFaq,
    AWFeature,
    AWHero,
    AWImage,
    AWItem,
    AWStep,
)
from headless_cms.serializers import LocalizedModelSerializer


class AWBaseSerializer(LocalizedModelSerializer):
    class Meta:
        extra_exclude = ["id", "position", "content_type", "object_id"]
        abstract = True


class AWImageSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWImage


class AWActionSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWAction


class AWItemSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWItem


class AWHeroSerializer(AWBaseSerializer):
    image = AWImageSerializer(read_only=True)
    actions = AWActionSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWHero


class AWFeatureSerializer(AWBaseSerializer):
    items = AWItemSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWFeature


class AWStepSerializer(AWBaseSerializer):
    image = AWImageSerializer(read_only=True)
    items = AWItemSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWStep


class AWFaqSerializer(AWBaseSerializer):
    items = AWItemSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWFaq


class AWCallToActionSerializer(AWBaseSerializer):
    actions = AWActionSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWCallToAction
