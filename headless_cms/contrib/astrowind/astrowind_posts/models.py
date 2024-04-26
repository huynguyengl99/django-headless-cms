import reversion
from django.db import models
from django.db.models import DateTimeField, F
from localized_fields.fields import (
    LocalizedCharField,
    LocalizedTextField,
)

from headless_cms.contrib.astrowind.astrowind_widgets.models import AWImage
from headless_cms.fields.martor_field import LocalizedMartorField
from headless_cms.models import LocalizedPublicationModel, LocalizedTitleSlugModel


@reversion.register(exclude=("published_version",))
class AWPostMetadata(LocalizedPublicationModel):
    title = LocalizedTextField(blank=True, null=True, required=False)
    description = LocalizedTextField(blank=True, null=True, required=False)
    canonical = LocalizedCharField(blank=True, null=True, required=False)


@reversion.register(exclude=("published_version",))
class AWPostImage(AWImage):
    pass


@reversion.register(exclude=("published_version",))
class AWPost(LocalizedPublicationModel):
    title = LocalizedTextField(blank=True, null=True, required=False)
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
        AWPostMetadata, blank=True, null=True, on_delete=models.SET_NULL
    )

    publish_date = DateTimeField(blank=True, null=True)
    updated_date = DateTimeField(auto_now=True)
    created_date = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = [F("publish_date").desc(nulls_first=True), "-created_date"]
        index_together = ["publish_date", "created_date"]


@reversion.register(exclude=("published_version",))
class AWCategory(LocalizedTitleSlugModel):
    pass


@reversion.register(exclude=("published_version",))
class AWPostTag(LocalizedTitleSlugModel):
    pass
