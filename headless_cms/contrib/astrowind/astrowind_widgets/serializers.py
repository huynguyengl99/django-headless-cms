from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from headless_cms.contrib.astrowind.astrowind_widgets.models import (
    AWBlogHighlightedPost,
    AWBlogLatestPost,
    AWBrand,
    AWCallToAction,
    AWContact,
    AWContent,
    AWContentAction,
    AWCtaAction,
    AWDisclaimer,
    AWFaq,
    AWFeature,
    AWFeature2,
    AWFeature3,
    AWFooter,
    AWFooterLink,
    AWFooterLinkItem,
    AWHeader,
    AWHeaderAction,
    AWHeaderLink,
    AWHeaderLinkThrough,
    AWHero,
    AWHeroAction,
    AWHeroText,
    AWHeroTextAction,
    AWInput,
    AWItem,
    AWPriceItem,
    AWPricing,
    AWStat,
    AWStatItem,
    AWStep,
    AWStep2,
    AWTestimonial,
    AWTestimonialItem,
    AWTextArea,
)
from headless_cms.contrib.astrowind.shared.serializers import AWBaseSerializer
from headless_cms.serializers import LocalizedModelSerializer


class AWBaseImageSerializer(AWBaseSerializer):
    src = serializers.SerializerMethodField()

    def get_src(self, obj):
        if obj.src:
            return self.context["request"].build_absolute_uri(obj.src.url)
        elif obj.src_url:
            return obj.src_url

    class Meta:
        abstract = True
        exclude = ["src_url"]


class AWItemSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWItem


class AWInputSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWInput


class AWTextAreaSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWTextArea


class AWDisclaimerSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWDisclaimer


class AWBaseFormSerializer(LocalizedModelSerializer):
    inputs = AWInputSerializer(read_only=True, many=True)
    textarea = AWTextAreaSerializer(read_only=True)
    disclaimer = AWDisclaimerSerializer(read_only=True)


class AWHeroActionSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWHeroAction


class AWHeroSerializer(AWBaseSerializer):
    actions = AWHeroActionSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWHero


class AWFeatureSerializer(AWBaseSerializer):
    items = AWItemSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWFeature


class AWStepSerializer(AWBaseSerializer):
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


class AWBrandSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWBrand


class AWContactSerializer(AWBaseFormSerializer, AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWContact


class AWContentActionSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWContentAction


class AWContentSerializer(AWBaseSerializer):
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


class AWHeaderLinkThroughSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWHeaderLinkThrough


class AWHeaderLinkSerializer(AWBaseSerializer):
    links = SerializerMethodField()

    class Meta(AWBaseSerializer.Meta):
        model = AWHeaderLink

    def get_links(self, obj):
        return self.__class__(obj.links.all(), many=True).data


class AWHeaderActionSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWHeaderAction


class AWHeaderSerializer(AWBaseSerializer):
    links = AWHeaderLinkSerializer(read_only=True, many=True)
    actions = AWHeaderActionSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWHeader


class AWFooterLinkItemSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWFooterLinkItem


class AWFooterLinkSerializer(AWBaseSerializer):
    links = AWFooterLinkItemSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWFooterLink


class AWFooterSerializer(AWBaseSerializer):
    links = AWFooterLinkSerializer(read_only=True, many=True)
    secondary_links = AWFooterLinkSerializer(read_only=True, many=True)
    social_links = AWFooterLinkSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWFooter


class AWHeroTextActionSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWHeroTextAction


class AWPriceItemActionSerializer(AWBaseSerializer):
    class Meta(AWBaseSerializer.Meta):
        model = AWHeroTextAction


class AWHeroTextSerializer(AWBaseSerializer):
    call_to_action = AWHeroTextActionSerializer(read_only=True)
    call_to_action2 = AWHeroTextActionSerializer(read_only=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWHeroText


class AWPriceItemSerializer(AWBaseSerializer):
    call_to_action = AWPriceItemActionSerializer(read_only=True)
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
    class Meta(AWBaseSerializer.Meta):
        model = AWTestimonialItem


class AWTestimonialSerializer(AWBaseSerializer):
    testimonials = AWTestimonialItemSerializer(read_only=True, many=True)

    class Meta(AWBaseSerializer.Meta):
        model = AWTestimonial
