from django.contrib import admin

from headless_cms.admin import EnhancedLocalizedVersionAdmin
from headless_cms.contrib.astrowind.astrowind_posts.models import AWPost, AWPostMetadata


@admin.register(AWPostMetadata)
class AWPostMetadataAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWPost)
class AWPostAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True
