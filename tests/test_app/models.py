import reversion
from django.db import models
from headless_cms.fields.martor_field import LocalizedMartorField
from headless_cms.models import PublicationModel
from localized_fields.fields import (
    LocalizedField,
    LocalizedTextField,
)
from localized_fields.models import LocalizedModel


@reversion.register(exclude=("published_version",))
class Post(LocalizedModel, PublicationModel):
    body = LocalizedMartorField(blank=False, null=False, required=False)
    title = LocalizedField(blank=False, null=False, required=False)
    description = LocalizedTextField(blank=False, null=False, required=False)


@reversion.register(exclude=("published_version",))
class Comment(LocalizedModel, PublicationModel):
    content = LocalizedMartorField(blank=False, null=False, required=False)
    title = LocalizedField(blank=False, null=False, required=False)
    post = models.ForeignKey(
        "test_app.Post",
        related_name="comments",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position"]
