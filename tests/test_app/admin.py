from adminsortable2.admin import SortableAdminBase, SortableStackedInline
from django.contrib import admin
from headless_cms.admin import EnhancedLocalizedVersionAdmin, PublishStatusInlineMixin

from test_app.models import Comment, Post


@admin.register(Comment)
class CommentAdmin(EnhancedLocalizedVersionAdmin):
    history_latest_first = True


class CommentInlineAdmin(
    PublishStatusInlineMixin,
    SortableStackedInline,
):
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(SortableAdminBase, EnhancedLocalizedVersionAdmin):
    history_latest_first = True


class PostWithComment(Post):
    class Meta:
        proxy = True


@admin.register(PostWithComment)
class PostWithCommentAdmin(SortableAdminBase, EnhancedLocalizedVersionAdmin):
    history_latest_first = True
    inlines = [CommentInlineAdmin]
