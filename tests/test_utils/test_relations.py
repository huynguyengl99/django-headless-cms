from headless_cms.utils.relations import calculate_prefetch_relation

from helpers.base import BaseTestCase
from test_app.models import Blog


class RelationTests(BaseTestCase):
    def test_calculate_prefetch_relation(self):
        prefetch_relations, select_relation = calculate_prefetch_relation(Blog)
        prefetches = {
            item if isinstance(item, str) else item.prefetch_to
            for item in prefetch_relations
        }
        assert prefetches == {
            "posts",
            "posts__tags",
            "posts__tags__published_version",
            "posts__published_version",
            "posts__category",
            "posts__category__published_version",
            "posts__items",
            "posts__items__published_version",
            "articles",
            "articles__images",
            "articles__images__published_version",
            "articles__published_version",
            "articles__items",
            "articles__items__published_version",
        }
        assert set(select_relation) == {
            "published_version",
            "domain",
            "domain__published_version",
        }
