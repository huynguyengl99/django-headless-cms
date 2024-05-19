import reversion
from django.db import models
from django.db.models import BooleanField, IntegerField
from django.utils.translation import gettext_lazy as _
from localized_fields.fields import (
    LocalizedCharField,
    LocalizedTextField,
)

from headless_cms.models import (
    LocalizedPublicationModel,
)


@reversion.register(exclude=("published_version",))
class AWMetadataRobot(LocalizedPublicationModel):
    index = BooleanField(default=False)
    follow = BooleanField(default=False)


@reversion.register(exclude=("published_version",))
class AWMetadataImage(LocalizedPublicationModel):
    url = LocalizedCharField(blank=True, null=True, required=False)
    width = IntegerField(default=0)
    height = IntegerField(default=0)


@reversion.register(exclude=("published_version",))
class AWMetaDataOpenGraph(LocalizedPublicationModel):
    url = LocalizedCharField(blank=True, null=True, required=False)
    site_name = LocalizedCharField(blank=True, null=True, required=False)
    images = models.ManyToManyField(
        AWMetadataImage, related_name="metadata_open_graphs"
    )
    locale = LocalizedCharField(blank=True, null=True, required=False)
    type = models.CharField(default="", blank=True)


@reversion.register(exclude=("published_version",))
class AWMetaDataTwitter(LocalizedPublicationModel):
    handle = LocalizedCharField(blank=True, null=True, required=False)
    site = LocalizedCharField(blank=True, null=True, required=False)
    card_type = LocalizedCharField(blank=True, null=True, required=False)


@reversion.register(exclude=("published_version",))
class AWMetadata(LocalizedPublicationModel):
    title = LocalizedTextField(blank=True, null=True, required=False)
    title_template = LocalizedTextField(
        default=dict,
        blank=True,
        null=True,
        required=False,
        help_text=_(
            "Title template (default should be %s - {title}), used for default site metadata."
        ),
    )
    description = LocalizedTextField(blank=True, null=True, required=False)
    canonical = LocalizedCharField(blank=True, null=True, required=False)
    ignore_title_template = BooleanField(default=False)
    robots = models.ForeignKey(
        AWMetadataRobot,
        blank=True,
        null=True,
        related_name="metadata",
        on_delete=models.SET_NULL,
    )
    open_graph = models.ForeignKey(
        AWMetaDataOpenGraph,
        blank=True,
        null=True,
        related_name="metadata",
        on_delete=models.SET_NULL,
    )
    twitter = models.ForeignKey(
        AWMetaDataTwitter,
        blank=True,
        null=True,
        related_name="metadata",
        on_delete=models.SET_NULL,
    )
