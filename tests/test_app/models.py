import reversion
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from headless_cms.fields.martor_field import LocalizedMartorField
from headless_cms.models import (
    LocalizedDynamicFileModel,
    LocalizedPublicationModel,
    LocalizedTitleSlugModel,
    M2MSortedOrderThrough,
    SortableGenericBaseModel,
)
from localized_fields.fields import (
    LocalizedTextField,
)


@reversion.register(exclude=("published_version",))
class Item(SortableGenericBaseModel):
    title = LocalizedTextField(blank=True, null=True, required=False)
    description = LocalizedTextField(blank=True, null=True, required=False)
    icon = models.CharField(blank=True, default="")


class News(LocalizedPublicationModel):
    title = LocalizedTextField(blank=True, null=True, required=False)
    subtitle = LocalizedTextField(blank=True, null=True, required=False)
    items = GenericRelation(Item)

    class Meta:
        abstract = True


@reversion.register(exclude=("published_version",))
class Post(News):
    description = LocalizedTextField(blank=True, null=True, required=False)
    body = LocalizedMartorField(blank=False, null=False, required=False)

    tags = models.ManyToManyField("PostTag", blank=True, related_name="posts")
    category = models.ForeignKey(
        "Category",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="posts",
    )


@reversion.register(exclude=("published_version",))
class Category(LocalizedTitleSlugModel):
    pass


@reversion.register(exclude=("published_version",))
class PostTag(LocalizedTitleSlugModel):
    pass


@reversion.register(exclude=("published_version",))
class Article(News):
    story = LocalizedMartorField(blank=False, null=False, required=False)
    images = models.ManyToManyField(
        "ArticleImage",
    )


@reversion.register(exclude=("published_version",))
class ArticleImage(LocalizedDynamicFileModel):
    pass


class ArticleSectionThrough(M2MSortedOrderThrough):
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    article_image = models.ForeignKey("ArticleImage", on_delete=models.CASCADE)
