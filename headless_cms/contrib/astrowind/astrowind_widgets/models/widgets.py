import reversion
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import CharField, Q
from django.utils.translation import gettext_lazy as _
from localized_fields.fields import (
    LocalizedCharField,
    LocalizedTextField,
)
from localized_fields.models import LocalizedModel

from headless_cms.models import PublicationModel


class AWGenericBaseModel(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(app_label="astrowind_widgets"),
        blank=True,
        null=True,
    )

    object = GenericForeignKey(
        ct_field="content_type",
        fk_field="object_id",
    )

    object_id = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self._meta.object_name} for {self.object}"

    @property
    def _content_type(self):
        return ContentType.objects.db_manager(self._state.db).get_for_id(
            self.content_type_id
        )

    @property
    def _model(self):
        return self._content_type.model_class()


@reversion.register(exclude=("published_version",))
class AWImage(LocalizedModel, PublicationModel):
    src = models.FileField()
    alt = LocalizedTextField()


@reversion.register(exclude=("published_version",))
class AWAction(LocalizedModel, PublicationModel, AWGenericBaseModel):
    class CTAVariants(models.TextChoices):
        PRIMARY = "primary", _("Primary")
        SECONDARY = "secondary", _("Secondary")
        TERTIARY = "tertiary", _("Tertiary")
        LINK = "link", _("Link")

    variant = models.CharField(choices=CTAVariants.choices, default=CTAVariants.PRIMARY)
    target = models.CharField(default="", blank=True)
    text = LocalizedCharField(default=dict, blank=True)
    href = CharField(default="", blank=True)
    icon = CharField(default="", blank=True)

    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position"]


@reversion.register(exclude=("published_version",))
class AWItem(LocalizedModel, PublicationModel, AWGenericBaseModel):
    title = LocalizedTextField()
    description = LocalizedTextField(blank=True, null=True, required=False)
    icon = models.CharField(blank=True, default="")

    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position"]


@reversion.register(exclude=("published_version",))
class AWHero(LocalizedModel, PublicationModel):
    title = LocalizedTextField()
    subtitle = LocalizedTextField(blank=True, null=True, required=False)
    tagline = LocalizedTextField(blank=True, null=True, required=False)
    content = LocalizedTextField(blank=True, null=True, required=False)
    image = models.ForeignKey(AWImage, blank=True, null=True, on_delete=models.SET_NULL)
    actions = GenericRelation(AWAction)


class AWSection(LocalizedModel, PublicationModel):
    title = LocalizedTextField()
    subtitle = LocalizedTextField(blank=True, null=True, required=False)
    tagline = LocalizedTextField(blank=True, null=True, required=False)
    html_id = models.CharField(default="", blank=True)

    items = GenericRelation(AWItem)

    class Meta:
        abstract = True


@reversion.register(exclude=("published_version",))
class AWFeature(AWSection):
    pass


@reversion.register(exclude=("published_version",))
class AWStep(AWSection):
    image = models.ForeignKey(AWImage, blank=True, null=True, on_delete=models.SET_NULL)


@reversion.register(exclude=("published_version",))
class AWFaq(AWSection):
    pass


@reversion.register(exclude=("published_version",))
class AWCallToAction(LocalizedModel, PublicationModel):
    title = LocalizedTextField()
    subtitle = LocalizedTextField(blank=True, null=True, required=False)
    actions = GenericRelation(AWAction)
