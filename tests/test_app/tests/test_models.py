import reversion
from reversion.models import Version

from test_app.models import Post
from test_utils.base import TestBase, TestModelMixin


class GetForModelTest(TestModelMixin, TestBase):
    def test_get_for_model(self):
        with reversion.create_revision():
            obj = Post.objects.create()
        assert Version.objects.get_for_model(obj.__class__).count() == 1
