from headless_cms.contrib.astrowind.astrowind_widgets.models import (
    AWAction,
    AWBlogHighlightedPost,
    AWBlogLatestPost,
    AWBrand,
    AWCallToAction,
    AWContact,
    AWContent,
    AWFaq,
    AWFeature,
    AWFeature2,
    AWFeature3,
    AWFooter,
    AWFooterLink,
    AWFooterLinkItem,
    AWHero,
    AWHeroText,
    AWImage,
    AWItem,
    AWPriceItem,
    AWPricing,
    AWStat,
    AWStatItem,
    AWStep,
    AWStep2,
    AWTestimonial,
    AWTestimonialItem,
)
from headless_cms.contrib.astrowind.shared.serializers import AWBaseSerializer


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


class AWBlogHighlightedPostSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWBlogHighlightedPost


class AWBlogLatestPostSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWBlogLatestPost


class AWBrandSerializer(AWBaseSerializer):
    images = AWImageSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWBrand


class AWContactSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWContact


class AWContentSerializer(AWBaseSerializer):
    image = AWImageSerializer(read_only=True)
    call_to_action = AWActionSerializer(read_only=True)
    items = AWItemSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWContent


class AWFeature2Serializer(AWBaseSerializer):
    items = AWItemSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWFeature2


class AWFeature3Serializer(AWBaseSerializer):
    items = AWItemSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWFeature3


class AWFooterLinkSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWFooterLink


class AWFooterLinkItemSerializer(AWBaseSerializer):
    footer_links = AWFooterLinkSerializer(read_only=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWFooterLinkItem


class AWFooterSerializer(AWBaseSerializer):
    links = AWFooterLinkSerializer(read_only=True, many=True)
    secondary_links = AWFooterLinkSerializer(read_only=True, many=True)
    social_links = AWFooterLinkSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWFooter


class AWHeroTextSerializer(AWBaseSerializer):
    call_to_action = AWCallToActionSerializer(read_only=True)
    call_to_action2 = AWCallToActionSerializer(read_only=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWHeroText


class AWPriceItemSerializer(AWBaseSerializer):
    call_to_action = AWCallToActionSerializer(read_only=True)
    items = AWItemSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWPriceItem


class AWPricingSerializer(AWBaseSerializer):
    prices = AWPriceItemSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWPricing


class AWStatItemSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWStatItem


class AWStatSerializer(AWBaseSerializer):
    stats = AWStatItemSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWStat


class AWStep2Serializer(AWBaseSerializer):
    call_to_action = AWCallToActionSerializer(read_only=True)
    items = AWItemSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWStep2


class AWTestimonialItemSerializer(AWBaseSerializer):
    image = AWImageSerializer(read_only=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWTestimonialItem


class AWTestimonialSerializer(AWBaseSerializer):
    testimonials = AWTestimonialItemSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWTestimonial
