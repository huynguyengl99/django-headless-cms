from headless_cms.contrib.astrowind.astrowind_pages.models import (
    AWAboutPage,
    AWIndexPage,
    AWPricingPage,
    AWSite,
)
from headless_cms.contrib.astrowind.astrowind_widgets.serializers import (
    AWCallToActionSerializer,
    AWContentSerializer,
    AWFaqSerializer,
    AWFeature2Serializer,
    AWFeature3Serializer,
    AWFeatureSerializer,
    AWFooterSerializer,
    AWHeaderSerializer,
    AWHeroSerializer,
    AWHeroTextSerializer,
    AWPricingSerializer,
    AWStatSerializer,
    AWStep2Serializer,
    AWStepSerializer,
)
from headless_cms.contrib.astrowind.shared.serializers import AWBaseSerializer


class AWIndexPageSerializer(AWBaseSerializer):
    hero = AWHeroSerializer(read_only=True)
    feature = AWFeatureSerializer(read_only=True)
    feature2 = AWFeature2Serializer(read_only=True)
    contents = AWContentSerializer(read_only=True, many=True)
    step = AWStepSerializer(read_only=True)
    faq = AWFaqSerializer(read_only=True)
    stat = AWStatSerializer(read_only=True)
    cta = AWCallToActionSerializer(read_only=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWIndexPage


class AWSiteSerializer(AWBaseSerializer):
    header = AWHeaderSerializer(read_only=True)
    footer = AWFooterSerializer(read_only=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWSite


class AWAboutPageSerializer(AWBaseSerializer):
    hero = AWHeroSerializer(read_only=True)
    stat = AWStatSerializer(read_only=True)

    feature3s = AWFeature3Serializer(read_only=True, many=True)
    step2s = AWStep2Serializer(read_only=True, many=True)
    feature2s = AWFeature2Serializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWAboutPage


class AWPricingPageSerializer(AWBaseSerializer):
    hero_text = AWHeroTextSerializer(read_only=True)
    prices = AWPricingSerializer(read_only=True)

    feature3 = AWFeature3Serializer(read_only=True)
    step = AWStepSerializer(read_only=True)
    faq = AWFaqSerializer(read_only=True)
    cta = AWCallToActionSerializer(read_only=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWPricingPage
