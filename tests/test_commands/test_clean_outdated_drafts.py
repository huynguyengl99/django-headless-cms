import reversion
from django.core.management import call_command
from reversion.models import Version

from helpers.base import BaseTestCase
from test_app.factories import PostFactory


class CleanOutdatedDraftsTests(BaseTestCase):
    def test_clean_outdated_drafts(self):
        with reversion.create_revision():
            post = PostFactory()

        with reversion.create_revision():
            post.title.en = "Other title"
            post.save()

        post.publish()

        with reversion.create_revision():
            post.title.en = "Another title"
            post.save()

        assert Version.objects.get_for_object(post).count() == 4

        call_command("clean_outdated_drafts")

        assert Version.objects.get_for_object(post).count() == 2
