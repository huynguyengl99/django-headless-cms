from django.contrib import admin
from django.contrib.admin import TabularInline

from headless_cms.admin import EnhancedLocalizedVersionAdmin, PublishStatusInlineMixin
from headless_cms.contrib.astrowind.astrowind_posts.models import (
    AWCategory,
    AWPost,
    AWPostImage,
    AWPostMetadata,
    AWPostTag,
)


@admin.register(AWPostMetadata)
class AWPostMetadataAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


class AWPostTagInline(
    PublishStatusInlineMixin,
    TabularInline,
):
    model = AWPost.tags.through
    extra = 0


@admin.register(AWPost)
class AWPostAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True
    exclude = ["tags"]
    inlines = [AWPostTagInline]


@admin.register(AWCategory)
class AWCategoryAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWPostImage)
class AWPostImageAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(AWPostTag)
class AWPostTagAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True
