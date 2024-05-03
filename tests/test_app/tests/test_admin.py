from unittest.mock import patch

import factory
import reversion
from django.conf import settings
from django.shortcuts import resolve_url
from django.utils import translation
from reversion.models import Version

from test_app.factories import PostFactory
from test_app.models import Post
from test_utils.base import BaseTestCase


class AdminChangeListViewTests(BaseTestCase):
    def test_render_change_list_view_with_unpublished_post(self):
        with reversion.create_revision():
            PostFactory.create()
        res = self.client.get(resolve_url("admin:test_app_post_changelist"))
        self.assertContains(res, Post.AdminPublishedStateHtml.UNPUBLISHED)

    def test_render_change_list_view_with_latest_published_post(self):
        with reversion.create_revision():
            post = PostFactory.create()
        post.publish(self.user)
        res = self.client.get(resolve_url("admin:test_app_post_changelist"))
        self.assertContains(res, Post.AdminPublishedStateHtml.PUBLISHED_LATEST)

    def test_render_change_list_view_with_outdated_published_post(self):
        with reversion.create_revision():
            post = PostFactory.create()
        post.publish(self.user)
        with reversion.create_revision():
            post.title = "new title"
            post.save()
        res = self.client.get(resolve_url("admin:test_app_post_changelist"))
        self.assertContains(res, Post.AdminPublishedStateHtml.PUBLISHED_OUTDATED)


class AdminChangeViewTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        with reversion.create_revision():
            self.obj: Post = PostFactory.create()

    def test_render_change_form_view_show_translate_button(self):
        res = self.client.get(resolve_url("admin:test_app_post_change", self.obj.id))

        self.assertContains(res, "Translate missing")
        self.assertContains(res, "Force re-translate")

    def test_render_change_form_view_unpublished(self):
        res = self.client.get(resolve_url("admin:test_app_post_change", self.obj.id))

        self.assertContains(res, "unpublished")
        self.assertContains(res, "Publish")
        self.assertNotContains(res, "Unpublish")

    def test_render_change_form_view_published_latest(self):
        self.obj.publish(self.user)
        res = self.client.get(resolve_url("admin:test_app_post_change", self.obj.id))

        self.assertContains(res, "published (latest)")
        self.assertNotContains(res, "Publish")
        self.assertContains(res, "Unpublish")

    def test_render_change_form_view_outdated_published(self):
        self.obj.publish(self.user)
        with reversion.create_revision():
            self.obj.title = "changed"
            self.obj.save()
        res = self.client.get(resolve_url("admin:test_app_post_change", self.obj.id))

        self.assertContains(res, "published (outdated)")
        self.assertContains(res, "Publish")
        self.assertContains(res, "Unpublish")


class AdminPostRequestTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        translation.activate(settings.LANGUAGE_CODE)
        dt = factory.build(dict, FACTORY_CLASS=PostFactory)
        self.localized_dt = {f"{k}_0": v for k, v in dt.items()}
        with reversion.create_revision():
            self.obj: Post = PostFactory.create(**dt)

    def test_publish_post(self):
        res = self.client.post(
            resolve_url("admin:test_app_post_change", self.obj.id),
            {"_publish": "Publish", **self.localized_dt},
        )
        self.obj.refresh_from_db()
        self.assertEqual(res.status_code, 302)
        self.assertIsNotNone(self.obj.published_version)

    def test_unpublish_post(self):
        self.obj.publish(self.user)
        res = self.client.post(
            resolve_url("admin:test_app_post_change", self.obj.id),
            {"_unpublish": "Unpublish", **self.localized_dt},
        )
        self.obj.refresh_from_db()
        self.assertEqual(res.status_code, 302)  # Check redirect
        self.assertIsNone(self.obj.published_version)

    def test_revert_post(self):
        old_title = str(self.obj.title)
        with reversion.create_revision():
            self.obj.title = "New title"
            self.obj.save()

        versions = Version.objects.get_for_object(self.obj)
        res = self.client.post(
            resolve_url("admin:test_app_post_revision", self.obj.id, versions[0].id),
            {**self.localized_dt},
        )
        self.obj.refresh_from_db()

        self.assertEqual(res.status_code, 302)  # Check redirect
        self.assertEqual(
            str(self.obj.title), old_title
        )  # The title should be the same as before the revert

        version: Version = Version.objects.get_for_object(self.obj).first()

        assert "Reverted to previous version" in version.revision.comment

    def test_revert_published_post(self):
        self.obj.publish(self.user)
        published_version_id = self.obj.published_version_id
        old_title = str(self.obj.title)

        with reversion.create_revision():
            self.obj.title = "New title"
            self.obj.save()

        versions = Version.objects.get_for_object(self.obj)
        res = self.client.post(
            resolve_url("admin:test_app_post_revision", self.obj.id, versions[0].id),
            {**self.localized_dt},
        )
        self.obj.refresh_from_db()

        self.assertEqual(res.status_code, 302)  # Check redirect
        self.assertEqual(
            str(self.obj.title), old_title
        )  # The title should be the same as before the revert

        version: Version = Version.objects.get_for_object(self.obj).first()

        assert "Reverted to previous version" in version.revision.comment
        assert self.obj.published_version_id == published_version_id

    @patch("headless_cms.auto_translate.BaseTranslate")
    def test_translate_post(self, mock_translate):
        res = self.client.post(
            resolve_url("admin:test_app_post_change", self.obj.id),
            {
                "_translate": "Translate",
                **self.localized_dt,
                # Include other fields as required
            },
        )
        self.obj.refresh_from_db()

        self.assertEqual(res.status_code, 302)  # Check redirect
        mock_translate.assert_called_with(self.obj)


class AdminAddViewTests(BaseTestCase):
    def test_add_view(self):
        dt = factory.build(dict, FACTORY_CLASS=PostFactory)
        localized_dt = {f"{k}_0": v for k, v in dt.items()}
        self.client.post(resolve_url("admin:test_app_post_add"), localized_dt)
        obj: Post = Post.objects.first()

        assert Version.objects.get_for_object(
            obj,
        ).exists()

        assert obj.published_state() == Post.AdminPublishedStateHtml.UNPUBLISHED


class AdminActionTests(BaseTestCase):
    def test_publish_action(self):
        with reversion.create_revision():
            obj: Post = PostFactory.create()
        with reversion.create_revision():
            obj2: Post = PostFactory.create()
        with reversion.create_revision():
            obj3: Post = PostFactory.create()

        assert not obj.published_version_id
        assert not obj2.published_version_id
        data = {"action": "publish", "_selected_action": [obj.id, obj2.id]}
        self.client.post(resolve_url("admin:test_app_post_changelist"), data)

        obj.refresh_from_db()
        obj2.refresh_from_db()
        obj3.refresh_from_db()

        assert obj.published_version_id
        assert obj2.published_version_id
        assert not obj3.published_version_id
