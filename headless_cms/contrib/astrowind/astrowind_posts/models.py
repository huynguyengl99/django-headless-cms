import reversion
from django.db import models
from django.db.models import DateTimeField, F
from localized_fields.fields import (
    LocalizedCharField,
    LocalizedTextField,
)

from headless_cms.contrib.astrowind.astrowind_metadata.models import AWMetadata
from headless_cms.fields import LocalizedMartorField
from headless_cms.models import (
    LocalizedDynamicFileModel,
    LocalizedTitleSlugModel,
    M2MSortedOrderThrough,
)


@reversion.register(exclude=("published_version",))
class AWPostImage(LocalizedDynamicFileModel):
    pass


@reversion.register(exclude=("published_version",))
class AWPost(LocalizedTitleSlugModel):
    excerpt = LocalizedTextField(blank=True, null=True, required=False)
    image = models.ForeignKey(
        AWPostImage,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="posts",
    )
    draft = models.BooleanField(default=False)
    category = models.ForeignKey(
        "AWCategory",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="posts",
    )
    tags = models.ManyToManyField("AWPostTag", blank=True, related_name="posts")
    author = LocalizedCharField(blank=True, null=True, required=False)

    content = LocalizedMartorField(default=dict, blank=True, null=True, required=False)

    metadata = models.ForeignKey(
        AWMetadata, blank=True, null=True, on_delete=models.SET_NULL
    )

    related_posts = models.ManyToManyField(
        "self",
        blank=True,
        through="AWRelatedPost",
        symmetrical=False,
    )

    publish_date = DateTimeField(blank=True, null=True)
    created_date = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = [F("publish_date").desc(nulls_first=True), "-created_date"]
        indexes = [
            models.Index(
                fields=["publish_date", "created_date"],
                name="awpost_publish_created_idx",
            )
        ]


class AWRelatedPost(M2MSortedOrderThrough):
    fk_name = "source_post"

    source_post = models.ForeignKey(
        AWPost, on_delete=models.CASCADE, related_name="source_through"
    )
    related_post = models.ForeignKey(
        AWPost, on_delete=models.CASCADE, related_name="related_through"
    )


@reversion.register(exclude=("published_version",))
class AWCategory(LocalizedTitleSlugModel):
    pass


@reversion.register(exclude=("published_version",))
class AWPostTag(LocalizedTitleSlugModel):
    pass
