import reversion
from django.utils import translation
from reversion.models import Version

from test_app.factories import CommentFactory, PostFactory
from test_app.models import Comment, Post
from test_utils.base import TestBase, TestModelMixin, TestModelParentMixin, UserMixin


class TestPublicationModel(UserMixin, TestModelParentMixin, TestModelMixin, TestBase):
    def test_not_published_model(self):
        with reversion.create_revision():
            obj = PostFactory.create()
        assert Version.objects.get_for_model(obj.__class__).count() == 1

        assert not obj.published_version
        assert not obj.published_data

        assert obj.published_state() == Post.AdminPublishedStateHtml.UNPUBLISHED

    def test_latest_published_model(self):
        translation.activate("en")

        with reversion.create_revision():
            obj: Post = PostFactory.create(title="Init title")

        obj.publish()

        assert obj.published_version
        assert obj.published_data
        assert obj.published_data["title"] == "Init title"
        assert obj.published_state() == Post.AdminPublishedStateHtml.PUBLISHED_LATEST

    def test_outdated_published_model(self):
        translation.activate("en")

        with reversion.create_revision():
            obj: Post = PostFactory.create(title="Init title")

        obj.publish(self.user)

        with reversion.create_revision():
            obj.title = "Outdated title"
            obj.save()

        assert obj.published_version
        assert obj.published_data
        assert obj.published_data["title"] == "Init title"
        assert obj.published_state() == Post.AdminPublishedStateHtml.PUBLISHED_OUTDATED

    def test_published_queryset(self):
        with reversion.create_revision():
            PostFactory.create()
        with reversion.create_revision():
            obj2 = PostFactory.create()
        obj2.publish()

        assert Post.objects.all().count() == 2
        assert Post.published_objects.published().count() == 1
        assert Post.published_objects.published().first() == obj2

    def test_related_query(self):
        # Create a published and an unpublished post
        with reversion.create_revision():
            post_published = PostFactory.create()
        post_published.publish()

        with reversion.create_revision():
            post_unpublished = PostFactory.create()

        # Create published and unpublished comments related to each post
        with reversion.create_revision():
            comment_published = CommentFactory.create(post=post_published)
        comment_published.publish()

        with reversion.create_revision():
            CommentFactory.create(post=post_published)

        with reversion.create_revision():
            comment_published_unpublished_post = CommentFactory.create(
                post=post_unpublished
            )
        comment_published_unpublished_post.publish()

        with reversion.create_revision():
            CommentFactory.create(post=post_unpublished)

        # Test the related query
        assert Post.objects.count() == 2
        posts_with_published_comments = Post.published_objects.published()
        assert len(posts_with_published_comments) == 1

        assert Comment.objects.count() == 4
        assert post_published.comments.count() == 2
        published_post = posts_with_published_comments[0]
        assert published_post.comments.count() == 1
        assert published_post.comments.first().id == comment_published.id
