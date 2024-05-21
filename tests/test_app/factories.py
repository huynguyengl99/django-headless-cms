import factory
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from factory.django import DjangoModelFactory
from faker import Faker

from test_app.models import (
    Article,
    ArticleImage,
    Blog,
    Category,
    Domain,
    Item,
    Post,
    PostTag,
)

f = Faker()


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.Faker("sentence", nb_words=3)


class PostTagFactory(DjangoModelFactory):
    class Meta:
        model = PostTag

    title = factory.Faker("sentence", nb_words=3)


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph", nb_sentences=3)
    body = factory.Faker("paragraph", nb_sentences=5)

    href = factory.LazyAttribute(lambda o: f"/{f.slug()}")


class ArticleFactory(DjangoModelFactory):
    class Meta:
        model = Article

    title = factory.Faker("sentence", nb_words=3)
    subtitle = factory.Faker("sentence", nb_words=5)
    story = factory.Faker("paragraph", nb_sentences=5)


class ArticleImageFactory(DjangoModelFactory):
    class Meta:
        model = ArticleImage

    src_file = {
        settings.LANGUAGE_CODE: factory.django.ImageField(color="blue").evaluate(
            None, None, {}
        )
    }
    src_url = factory.Faker("image_url")
    alt = factory.Faker("sentence", nb_words=3)


class ItemFactory(DjangoModelFactory):
    class Meta:
        model = Item

    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph", nb_sentences=3)
    icon = factory.Faker("word")


class GenericItemFactory(ItemFactory):
    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph", nb_sentences=3)
    icon = factory.Faker("word")

    object_id = factory.SelfAttribute("content_object.id")
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object)
    )

    class Meta:
        exclude = ["content_object"]
        abstract = True


class PostItemFactory(GenericItemFactory):
    content_object = factory.SubFactory(PostFactory)

    class Meta:
        model = Item


class ArticleItemFactory(GenericItemFactory):
    content_object = factory.SubFactory(ArticleFactory)

    class Meta:
        model = Item


class DomainFactory(DjangoModelFactory):
    class Meta:
        model = Domain

    title = factory.Faker("sentence", nb_words=3)
    slug = factory.Faker("slug")


class BlogFactory(DjangoModelFactory):
    class Meta:
        model = Blog

    name = factory.Faker("sentence", nb_words=3)
    domain = factory.SubFactory(DomainFactory)
