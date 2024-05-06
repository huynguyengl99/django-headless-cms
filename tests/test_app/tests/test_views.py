import reversion
from django.urls import reverse
from rest_framework import status

from helpers.base import BaseAPITestCase
from test_app.factories import (  # assuming you have a factory for Post model
    CategoryFactory,
    PostFactory,
)
from test_app.models import Post


class PostCMSViewSetTest(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        with reversion.create_revision():
            self.category = CategoryFactory.create()

        with reversion.create_revision():
            self.published_post: Post = PostFactory.create(category=self.category)
        self.published_post.publish()
        with reversion.create_revision():
            self.unpublished_post = PostFactory.create()
        self.url = reverse("posts-list")

    def test_list_published_posts(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]["id"], self.published_post.id)

    def test_unpublished_posts_not_returned(self):
        response = self.client.get(self.url)

        # Check that the unpublished post is not in the returned data
        self.assertNotIn(
            self.unpublished_post.id, [post["id"] for post in response.data]
        )
