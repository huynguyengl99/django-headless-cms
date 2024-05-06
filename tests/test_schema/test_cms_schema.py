from unittest import mock

from django.urls import reverse

from helpers.base import BaseAPITestCase
from helpers.schema_utils import assert_api_schema


@mock.patch("drf_spectacular.settings.spectacular_settings.SCHEMA_PATH_PREFIX", "")
class TestCMSSpectacularAPIView(BaseAPITestCase):
    def test_schema(self):
        res = self.client.get(reverse("cms-schema"))

        assert_api_schema(res.content, "test_schema/test_cms_api_schema.yml")
