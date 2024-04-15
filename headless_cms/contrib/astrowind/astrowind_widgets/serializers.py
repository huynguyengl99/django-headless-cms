from headless_cms.contrib.astrowind.astrowind_widgets.models import (
    AWBlogHighlightedPost,
    AWBlogLatestPost,
    AWBrand,
    AWBrandImage,
    AWCallToAction,
    AWContact,
    AWContent,
    AWContentAction,
    AWContentImage,
    AWCtaAction,
    AWFaq,
    AWFeature,
    AWFeature2,
    AWFeature3,
    AWFooter,
    AWFooterLink,
    AWFooterLinkItem,
    AWHero,
    AWHeroAction,
    AWHeroImage,
    AWHeroText,
    AWItem,
    AWPriceItem,
    AWPricing,
    AWStat,
    AWStatItem,
    AWStep,
    AWStep2,
    AWStepImage,
    AWTestimonial,
    AWTestimonialItem,
    AWTestimonialItemImage,
)
from headless_cms.contrib.astrowind.shared.serializers import AWBaseSerializer


class AWItemSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWItem


class AWHeroImageSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWHeroImage


class AWHeroActionSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWHeroAction


class AWHeroSerializer(AWBaseSerializer):
    image = AWHeroImageSerializer(read_only=True)
    actions = AWHeroActionSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWHero


class AWFeatureSerializer(AWBaseSerializer):
    items = AWItemSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWFeature


class AWStepImageSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWStepImage


class AWStepSerializer(AWBaseSerializer):
    image = AWStepImageSerializer(read_only=True)
    items = AWItemSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWStep


class AWFaqSerializer(AWBaseSerializer):
    items = AWItemSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWFaq


class AWCtaActionSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWCtaAction


class AWCallToActionSerializer(AWBaseSerializer):
    actions = AWCtaActionSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWCallToAction


class AWBlogHighlightedPostSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWBlogHighlightedPost


class AWBlogLatestPostSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWBlogLatestPost


class AWBrandImageSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWBrandImage


class AWBrandSerializer(AWBaseSerializer):
    images = AWBrandImageSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWBrand


class AWContactSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWContact


class AWContentImageSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWContentImage


class AWContentActionSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWContentAction


class AWContentSerializer(AWBaseSerializer):
    image = AWContentImageSerializer(read_only=True)
    call_to_action = AWContentActionSerializer(read_only=True)
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


class AWTestimonialItemImageSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWTestimonialItemImage


class AWTestimonialItemSerializer(AWBaseSerializer):
    image = AWTestimonialItemImageSerializer(read_only=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWTestimonialItem


class AWTestimonialSerializer(AWBaseSerializer):
    testimonials = AWTestimonialItemSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWTestimonial
