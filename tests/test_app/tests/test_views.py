import reversion
from django.urls import reverse
from rest_framework import status

from test_app.factories import PostFactory  # assuming you have a factory for Post model
from test_app.models import Post
from test_utils.base import BaseAPITestCase


class PostCMSViewSetTest(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        with reversion.create_revision():
            self.published_post: Post = PostFactory.create()
        self.published_post.publish()
        with reversion.create_revision():
            self.unpublished_post = PostFactory.create()
        self.url = reverse("posts-list")

    def test_list_published_posts(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data), 1
        )  # only one published post should be returned

        # Check that the published post is returned
        self.assertEqual(response.data[0]["id"], self.published_post.id)

    def test_unpublished_posts_not_returned(self):
        response = self.client.get(self.url)

        # Check that the unpublished post is not in the returned data
        self.assertNotIn(
            self.unpublished_post.id, [post["id"] for post in response.data]
        )
