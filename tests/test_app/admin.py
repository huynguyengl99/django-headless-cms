from headless_cms.admin import auto_admins

from test_app.models import Article, ArticleImage, Category, Item, Post, PostTag

auto_admins([Article, ArticleImage, Category, Item, Post, PostTag])
