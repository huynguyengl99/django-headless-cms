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
    AWHeroTextAction2,
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


class AWHeroImageInline(
    PublishStatusInlineMixin,
    StackedInline,
):
    model = AWHeroImage
    extra = 0


@admin.register(AWHero)
class AWHeroAdmin(SortableAdminBase, EnhancedLocalizedVersionAdmin):
    history_latest_first = True

    inlines = [AWHeroActionInline, AWHeroImageInline]


@admin.register(AWItem)
class AWItemAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True
    list_filter = ("content_type",)


@admin.register(AWStepImage)
class AWStepImageAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


class AWStepImageInline(
    PublishStatusInlineMixin,
    StackedInline,
):
    model = AWStepImage
    extra = 0


@admin.register(AWStep)
class AWStepAdmin(AWSectionAdmin):
    history_latest_first = True
    inlines = AWSectionAdmin.inlines + [AWStepImageInline]


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
class AWContactAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWContentAction)
class AWContentActionAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


class AWContentActionInline(
    PublishStatusInlineMixin,
    StackedInline,
):
    model = AWContentAction
    extra = 0


@admin.register(AWContentImage)
class AWContentImageAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


class AWContentImageInline(
    PublishStatusInlineMixin,
    StackedInline,
):
    model = AWContentImage
    extra = 0


@admin.register(AWContent)
class AWContentAdmin(AWSectionAdmin):
    history_latest_first = True
    inlines = AWSectionAdmin.inlines + [AWContentActionInline, AWContentImageInline]


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


class AWHeroTextActionInline(
    PublishStatusInlineMixin,
    StackedInline,
):
    model = AWHeroTextAction
    extra = 0


@admin.register(AWHeroTextAction2)
class AWHeroTextAction2Admin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


class AWHeroTextAction2Inline(
    PublishStatusInlineMixin,
    StackedInline,
):
    model = AWHeroTextAction2
    extra = 0


@admin.register(AWHeroText)
class AWHeroTextAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True

    inlines = [AWHeroTextActionInline, AWHeroTextAction2Inline]


@admin.register(AWInput)
class AWInputAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWPriceItemAction)
class AWPriceItemActionAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


class AWPriceItemActionInline(
    PublishStatusInlineMixin,
    StackedInline,
):
    model = AWPriceItemAction
    extra = 0


@admin.register(AWPriceItem)
class AWPriceItemAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True
    inlines = [AWPriceItemActionInline]


@admin.register(AWPricing)
class AWPricingAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


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


class AWStep2ActionInline(
    PublishStatusInlineMixin,
    StackedInline,
):
    model = AWStep2Action
    extra = 0


@admin.register(AWStep2)
class AWStep2Admin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True
    inlines = [AWStep2ActionInline]


@admin.register(AWTextArea)
class AWTextAreaAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWTestimonialItemImage)
class AWTestimonialItemImageAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


class AWTestimonialItemImageInline(
    PublishStatusInlineMixin,
    StackedInline,
):
    model = AWTestimonialItemImage
    extra = 0


@admin.register(AWTestimonialItem)
class AWTestimonialItemAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True
    inlines = [AWTestimonialItemImageInline]


class AWTestimonialItemInline(
    PublishStatusInlineMixin,
    SortableStackedInline,
):
    model = AWTestimonialItem
    fields = ["id"]


@admin.register(AWTestimonialAction)
class AWTestimonialActionAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


class AWTestimonialActionInline(
    PublishStatusInlineMixin,
    StackedInline,
):
    model = AWTestimonialAction
    extra = 0


@admin.register(AWTestimonial)
class AWTestimonialAdmin(SortableAdminBase, EnhancedLocalizedVersionAdmin):
    history_latest_first = True
    inlines = [AWTestimonialActionInline, AWTestimonialItemInline]
