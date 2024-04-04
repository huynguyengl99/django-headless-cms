from test_app.factories import PostFactory
from test_app.serializers import PostSerializer
from test_utils.base import BaseTestCase


class TestLocalizedSerializer(BaseTestCase):
    def test_no_published_data(self):
        post = PostFactory()

        serializer = PostSerializer()
        assert serializer.to_representation(post) is None
