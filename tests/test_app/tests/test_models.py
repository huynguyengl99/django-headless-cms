from unittest.mock import Mock, call

import reversion
from django.utils import translation
from reversion.models import Version

from helpers.base import BaseTestCase
from test_app.factories import (
    ArticleFactory,
    BlogFactory,
    NoteFactory,
    PostFactory,
)
from test_app.models import Article, Blog, Post


class TestPublicationModel(BaseTestCase):
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
        translation.deactivate()

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
        translation.deactivate()

    def test_published_queryset(self):
        with reversion.create_revision():
            PostFactory.create()
        with reversion.create_revision():
            obj2 = PostFactory.create()
        obj2.publish()

        assert Post.objects.all().count() == 2
        assert Post.published_objects.published().count() == 1
        assert Post.published_objects.published().first() == obj2

    def test_recursive_action(self):
        with reversion.create_revision():
            self.note = NoteFactory.create()

        with reversion.create_revision():
            self.post: Post = PostFactory.create(note=self.note)

        with reversion.create_revision():
            self.article: Article = ArticleFactory.create(note=self.note)

        with reversion.create_revision():
            self.blog: Blog = BlogFactory.create()

        self.blog.articles.add(self.article)
        self.blog.posts.add(self.post)

        action = Mock()

        self.blog.recursive_action(action)

        action.assert_has_calls(
            [
                call(self.blog),
                call(self.post),
                call(self.note),
                call(self.article),
            ],
            any_order=True,
        )  # note only call once because we have deduplicated
