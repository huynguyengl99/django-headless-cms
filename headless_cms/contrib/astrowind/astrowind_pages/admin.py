from django.contrib import admin
from solo.admin import SingletonModelAdmin

from headless_cms.admin import EnhancedLocalizedVersionAdmin
from headless_cms.contrib.astrowind.astrowind_pages.models import (
    AWIndexPage,
)


@admin.register(AWIndexPage)
class AWIndexPageAdmin(EnhancedLocalizedVersionAdmin, SingletonModelAdmin):
    history_latest_first = True
