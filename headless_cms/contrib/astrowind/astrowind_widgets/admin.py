from adminsortable2.admin import (
    SortableAdminBase,
    SortableGenericInlineAdminMixin,
    SortableInlineAdminMixin,
    SortableStackedInline,
)
from django.contrib import admin
from django.contrib.admin import StackedInline
from django.contrib.contenttypes.admin import GenericStackedInline

from headless_cms.admin import EnhancedLocalizedVersionAdmin, PublishStatusInlineMixin
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
    AWHero,
    AWHeroAction,
    AWHeroImage,
    AWHeroText,
    AWHeroTextAction,
    AWInput,
    AWItem,
    AWPriceItem,
    AWPriceItemAction,
    AWPricing,
    AWStat,
    AWStatItem,
    AWStep,
    AWStep2,
    AWStep2Action,
    AWStepImage,
    AWTestimonial,
    AWTestimonialAction,
    AWTestimonialItem,
    AWTestimonialItemImage,
    AWTextArea,
)


class BaseSortablePublishGenericAdmin(
    PublishStatusInlineMixin,
    SortableGenericInlineAdminMixin,
    SortableStackedInline,
    GenericStackedInline,
):
    extra = 0


class AWItemInline(BaseSortablePublishGenericAdmin):
    model = AWItem


class AWInputInline(BaseSortablePublishGenericAdmin):
    model = AWInput


class AWContentInline(BaseSortablePublishGenericAdmin):
    model = AWContent
    fields = ["id"]


class AWStatItemInline(
    PublishStatusInlineMixin,
    SortableStackedInline,
):
    model = AWStatItem
    extra = 0


@admin.register(AWCtaAction)
class AWCTAActionAdmin(SortableAdminBase, EnhancedLocalizedVersionAdmin):
    history_latest_first = True


class AWCtaActionInline(
    PublishStatusInlineMixin,
    SortableStackedInline,
):
    model = AWCtaAction
    extra = 0


@admin.register(AWCallToAction)
class AWCallToActionAdmin(SortableAdminBase, EnhancedLocalizedVersionAdmin):
    history_latest_first = True

    inlines = [AWCtaActionInline]


class AWSectionAdmin(SortableAdminBase, EnhancedLocalizedVersionAdmin):
    history_latest_first = True

    inlines = [AWItemInline]

    class Meta:
        abstract = True


@admin.register(AWFaq)
class AWFaqsAdmin(AWSectionAdmin):
    history_latest_first = True


@admin.register(AWFeature)
class AWFeatureAdmin(AWSectionAdmin):
    history_latest_first = True


@admin.register(AWHeroAction)
class AWHeroActionActionAdmin(SortableAdminBase, EnhancedLocalizedVersionAdmin):
    history_latest_first = True


class AWHeroActionInline(
    PublishStatusInlineMixin,
    SortableStackedInline,
):
    model = AWHeroAction
    extra = 0


@admin.register(AWHeroImage)
class AWHeroImageAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWHero)
class AWHeroAdmin(SortableAdminBase, EnhancedLocalizedVersionAdmin):
    history_latest_first = True

    inlines = [AWHeroActionInline]


@admin.register(AWItem)
class AWItemAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True
    list_filter = ("content_type",)


@admin.register(AWStepImage)
class AWStepImageAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWStep)
class AWStepAdmin(AWSectionAdmin):
    history_latest_first = True


@admin.register(AWBlogHighlightedPost)
class AWBlogHighlightedPostAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWBlogLatestPost)
class AWBlogLatestPostAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWBrandImage)
class AWBrandImageAdmin(SortableAdminBase, EnhancedLocalizedVersionAdmin):
    history_latest_first = True


class AWBrandImageInline(
    PublishStatusInlineMixin,
    SortableStackedInline,
):
    model = AWBrandImage
    extra = 0


@admin.register(AWBrand)
class AWBrandAdmin(SortableAdminBase, EnhancedLocalizedVersionAdmin):
    history_latest_first = True

    inlines = [AWBrandImageInline]


@admin.register(AWContact)
class AWContactAdmin(SortableAdminBase, EnhancedLocalizedVersionAdmin):
    history_latest_first = True

    inlines = [AWInputInline]


@admin.register(AWContentAction)
class AWContentActionAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWContentImage)
class AWContentImageAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWContent)
class AWContentAdmin(AWSectionAdmin):
    history_latest_first = True


@admin.register(AWFeature2)
class AWFeature2Admin(AWSectionAdmin):
    history_latest_first = True


@admin.register(AWFeature3)
class AWFeature3Admin(AWSectionAdmin):
    history_latest_first = True


class AWHeaderLinkSelfInline(
    PublishStatusInlineMixin,
    SortableInlineAdminMixin,
    StackedInline,
):
    model = AWHeaderLink.links.through
    fk_name = "parent_link"
    extra = 0


@admin.register(AWHeaderLink)
class AWHeaderLinkAdmin(SortableAdminBase, EnhancedLocalizedVersionAdmin):
    history_latest_first = True

    inlines = [AWHeaderLinkSelfInline]


@admin.register(AWHeaderAction)
class AWHeaderActionAdmin(SortableAdminBase, EnhancedLocalizedVersionAdmin):
    history_latest_first = True


class AWHeaderLinkInline(
    PublishStatusInlineMixin,
    SortableInlineAdminMixin,
    StackedInline,
):
    model = AWHeader.links.through
    extra = 0


class AWHeaderActionInline(
    PublishStatusInlineMixin,
    SortableInlineAdminMixin,
    StackedInline,
):
    model = AWHeader.actions.through

    extra = 0


@admin.register(AWHeader)
class AWHeaderAdmin(SortableAdminBase, EnhancedLocalizedVersionAdmin):
    history_latest_first = True

    inlines = [AWHeaderLinkInline, AWHeaderActionInline]


@admin.register(AWFooterLinkItem)
class AWFooterLinkItemAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


class AWFooterLinkItemInline(
    PublishStatusInlineMixin,
    SortableInlineAdminMixin,
    StackedInline,
):
    model = AWFooterLinkItem
    extra = 0


@admin.register(AWFooterLink)
class AWFooterLinkAdmin(SortableAdminBase, EnhancedLocalizedVersionAdmin):
    history_latest_first = True

    inlines = [AWFooterLinkItemInline]


class AWFooterLinkInlineBase(
    PublishStatusInlineMixin,
    SortableInlineAdminMixin,
    StackedInline,
):
    extra = 0


class AWFooterLinksInline(AWFooterLinkInlineBase):
    model = AWFooter.links.through
    extra = 0

    verbose_name = "Link"


class AWFooterSecondaryLinksInline(AWFooterLinkInlineBase):
    model = AWFooter.secondary_links.through
    extra = 0

    verbose_name = "Secondary link"


class AWFooterSocialLinksInline(AWFooterLinkInlineBase):
    model = AWFooter.social_links.through
    extra = 0
    verbose_name = "Social link"


@admin.register(AWFooter)
class AWFooterAdmin(SortableAdminBase, EnhancedLocalizedVersionAdmin):
    history_latest_first = True

    inlines = [
        AWFooterLinksInline,
        AWFooterSecondaryLinksInline,
        AWFooterSocialLinksInline,
    ]


@admin.register(AWHeroTextAction)
class AWHeroTextActionAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWHeroText)
class AWHeroTextAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWInput)
class AWInputAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWPriceItemAction)
class AWPriceItemActionAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWPriceItem)
class AWPriceItemAdmin(SortableAdminBase, EnhancedLocalizedVersionAdmin):
    history_latest_first = True

    inlines = [AWItemInline]


class AWPriceItemInline(
    PublishStatusInlineMixin,
    SortableInlineAdminMixin,
    StackedInline,
):
    model = AWPricing.prices.through
    extra = 0


@admin.register(AWPricing)
class AWPricingAdmin(SortableAdminBase, EnhancedLocalizedVersionAdmin):
    history_latest_first = True

    inlines = [AWPriceItemInline]


@admin.register(AWStatItem)
class AWStatItemAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWStat)
class AWStatAdmin(SortableAdminBase, EnhancedLocalizedVersionAdmin):
    history_latest_first = True

    inlines = [AWStatItemInline]


@admin.register(AWStep2Action)
class AWStep2ActionAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWStep2)
class AWStep2Admin(AWSectionAdmin):
    history_latest_first = True


@admin.register(AWDisclaimer)
class AWDisclaimerAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWTextArea)
class AWTextAreaAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWTestimonialItemImage)
class AWTestimonialItemImageAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWTestimonialItem)
class AWTestimonialItemAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWTestimonialAction)
class AWTestimonialActionAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWTestimonial)
class AWTestimonialAdmin(SortableAdminBase, EnhancedLocalizedVersionAdmin):
    history_latest_first = True
