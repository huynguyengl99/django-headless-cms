from adminsortable2.admin import (
    SortableAdminBase,
    SortableGenericInlineAdminMixin,
    SortableStackedInline,
)
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from headless_cms.admin import EnhancedLocalizedVersionAdmin, PublishStatusInlineMixin
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


@admin.register(AWAction)
class AWActionAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True
    list_filter = ("content_type",)


class AWActionInline(
    PublishStatusInlineMixin,
    SortableGenericInlineAdminMixin,
    SortableStackedInline,
    GenericStackedInline,
):
    model = AWAction
    extra = 0


class AWItemInline(
    PublishStatusInlineMixin,
    SortableGenericInlineAdminMixin,
    SortableStackedInline,
    GenericStackedInline,
):
    model = AWItem
    extra = 0


class AWStatItemInline(
    PublishStatusInlineMixin,
    SortableStackedInline,
):
    model = AWStatItem
    extra = 0


@admin.register(AWCallToAction)
class AWCallToActionAdmin(SortableAdminBase, EnhancedLocalizedVersionAdmin):
    history_latest_first = True

    inlines = [AWActionInline]


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


@admin.register(AWHero)
class AWHeroAdmin(SortableAdminBase, EnhancedLocalizedVersionAdmin):
    history_latest_first = True

    inlines = [AWActionInline]


@admin.register(AWImage)
class AWImageAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWItem)
class AWItemAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True
    list_filter = ("content_type",)


@admin.register(AWStep)
class AWStepAdmin(AWSectionAdmin):
    history_latest_first = True


@admin.register(AWBlogHighlightedPost)
class AWBlogHighlightedPostAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWBlogLatestPost)
class AWBlogLatestPostAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWBrand)
class AWBrandAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWContact)
class AWContactAdmin(EnhancedLocalizedVersionAdmin):
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


@admin.register(AWFooter)
class AWFooterAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWFooterLink)
class AWFooterLinkAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWFooterLinkItem)
class AWFooterLinkItemAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWHeroText)
class AWHeroTextAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWInput)
class AWInputAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWPriceItem)
class AWPriceItemAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


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


@admin.register(AWStep2)
class AWStep2Admin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWTextArea)
class AWTextAreaAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWTestimonialItem)
class AWTestimonialItemAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWTestimonial)
class AWTestimonialAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True
