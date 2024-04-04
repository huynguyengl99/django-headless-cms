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
    AWCallToAction,
    AWFaq,
    AWFeature,
    AWHero,
    AWImage,
    AWItem,
    AWStep,
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
