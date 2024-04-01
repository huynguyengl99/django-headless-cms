import factory
from factory.django import DjangoModelFactory

from test_app.models import Comment, Post


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph", nb_sentences=3)
    body = factory.Faker("paragraph", nb_sentences=3)


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    title = factory.Faker("sentence", nb_words=3)
    content = factory.Faker("paragraph", nb_sentences=3)
    post = factory.SubFactory(PostFactory)
