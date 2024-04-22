from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from django.contrib import admin
from django.contrib.admin import StackedInline
from solo.admin import SingletonModelAdmin

from headless_cms.admin import EnhancedLocalizedVersionAdmin, PublishStatusInlineMixin
from headless_cms.contrib.astrowind.astrowind_pages.models import (
    AWAboutPage,
    AWContactPage,
    AWIndexPage,
    AWPricingPage,
    AWSite,
)
from headless_cms.contrib.astrowind.astrowind_widgets.admin import AWContentInline


@admin.register(AWIndexPage)
class AWIndexPageAdmin(
    SortableAdminBase, EnhancedLocalizedVersionAdmin, SingletonModelAdmin
):
    history_latest_first = True

    inlines = [AWContentInline]


@admin.register(AWSite)
class AWSiteAdmin(EnhancedLocalizedVersionAdmin, SingletonModelAdmin):
    history_latest_first = True


class AWAboutFeature3Inline(
    PublishStatusInlineMixin,
    SortableInlineAdminMixin,
    StackedInline,
):
    model = AWAboutPage.feature3s.through
    extra = 0


class AWAboutFeature2Inline(
    PublishStatusInlineMixin,
    SortableInlineAdminMixin,
    StackedInline,
):
    model = AWAboutPage.feature2s.through
    extra = 0


class AWAboutStep2Inline(
    PublishStatusInlineMixin,
    SortableInlineAdminMixin,
    StackedInline,
):
    model = AWAboutPage.step2s.through
    extra = 0


@admin.register(AWAboutPage)
class AWAboutPageAdmin(
    SortableAdminBase, EnhancedLocalizedVersionAdmin, SingletonModelAdmin
):
    history_latest_first = True

    inlines = [AWAboutFeature3Inline, AWAboutStep2Inline, AWAboutFeature2Inline]


@admin.register(AWPricingPage)
class AWPricingPageAdmin(EnhancedLocalizedVersionAdmin, SingletonModelAdmin):
    history_latest_first = True


@admin.register(AWContactPage)
class AWContactPageAdmin(EnhancedLocalizedVersionAdmin, SingletonModelAdmin):
    history_latest_first = True
