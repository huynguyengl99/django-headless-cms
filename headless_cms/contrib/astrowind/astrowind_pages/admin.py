from adminsortable2.admin import SortableAdminBase
from django.contrib import admin
from solo.admin import SingletonModelAdmin

from headless_cms.admin import EnhancedLocalizedVersionAdmin
from headless_cms.contrib.astrowind.astrowind_pages.models import (
    AWIndexPage,
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
