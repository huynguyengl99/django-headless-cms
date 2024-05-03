from adminsortable2.admin import (
    SortableAdminBase,
    SortableInlineAdminMixin,
)
from django.contrib import admin
from django.contrib.admin import StackedInline

from headless_cms.admin import (
    EnhancedLocalizedVersionAdmin,
    PublishStatusInlineMixin,
    auto_admins,
)
from headless_cms.contrib.astrowind.astrowind_widgets.models import (
    AWAction,
    AWBlogHighlightedPost,
    AWBlogLatestPost,
    AWBrand,
    AWCallToAction,
    AWContact,
    AWContent,
    AWDisclaimer,
    AWFaq,
    AWFeature,
    AWFeature2,
    AWFeature3,
    AWFooter,
    AWFooterLink,
    AWFooterLinkItem,
    AWHeader,
    AWHeaderLink,
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


auto_admins(
    [
        AWAction,
        AWBlogHighlightedPost,
        AWBlogLatestPost,
        AWBrand,
        AWCallToAction,
        AWContact,
        AWContent,
        AWDisclaimer,
        AWFaq,
        AWFeature,
        AWFeature2,
        AWFeature3,
        AWFooter,
        AWFooterLink,
        AWFooterLinkItem,
        AWHeader,
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
    ]
)
