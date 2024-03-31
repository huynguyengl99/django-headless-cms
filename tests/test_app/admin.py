from django.contrib import admin
from headless_cms.admin import EnhancedLocalizedVersionAdmin

from test_app.models import Comment, Post


@admin.register(Post)
class PostAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


@admin.register(Comment)
class CommentAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True
