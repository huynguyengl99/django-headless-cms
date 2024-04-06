import reversion
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import CharField, IntegerField, Q
from django.utils.translation import gettext_lazy as _
from localized_fields.fields import (
    LocalizedCharField,
    LocalizedTextField,
)
from localized_fields.models import LocalizedModel

from headless_cms.models import PublicationModel


class AWGenericBaseModel(models.Model):
    limit = Q(app_label="astrowind_widgets")

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=limit,
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
        return f"{self._meta.object_name} - {self.id} for {self.object}"

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
    alt = LocalizedTextField(blank=True, null=True, required=False)


@reversion.register(exclude=("published_version",))
class AWAction(LocalizedModel, PublicationModel, AWGenericBaseModel):
    class CTAVariants(models.TextChoices):
        PRIMARY = "primary", _("Primary")
        SECONDARY = "secondary", _("Secondary")
        TERTIARY = "tertiary", _("Tertiary")
        LINK = "link", _("Link")

    variant = models.CharField(choices=CTAVariants.choices, default=CTAVariants.PRIMARY)
    target = models.CharField(default="", blank=True)
    text = LocalizedCharField(blank=True, null=True, required=False)
    href = CharField(default="", blank=True)
    icon = CharField(default="", blank=True)

    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position"]


@reversion.register(exclude=("published_version",))
class AWItem(LocalizedModel, PublicationModel, AWGenericBaseModel):
    title = LocalizedTextField(blank=True, null=True, required=False)
    description = LocalizedTextField(blank=True, null=True, required=False)
    icon = models.CharField(blank=True, default="")

    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position"]


@reversion.register(exclude=("published_version",))
class AWInput(LocalizedModel, PublicationModel, AWGenericBaseModel):
    type = CharField(default="text", blank=True)
    name = CharField()
    label = LocalizedCharField(blank=True, null=True, required=False)
    autocomplete = CharField(default="on", blank=True)
    placeholder = LocalizedCharField(blank=True, null=True, required=False)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position"]


@reversion.register(exclude=("published_version",))
class AWTextArea(LocalizedModel, PublicationModel, AWGenericBaseModel):
    name = CharField()
    label = LocalizedCharField(blank=True, null=True, required=False)
    rows = IntegerField(default=4)
    placeholder = LocalizedCharField(blank=True, null=True, required=False)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position"]


class AWFragment(LocalizedModel, PublicationModel):
    title = LocalizedTextField(blank=True, null=True, required=False)
    subtitle = LocalizedTextField(blank=True, null=True, required=False)
    tagline = LocalizedTextField(blank=True, null=True, required=False)
    html_id = models.CharField(default="", blank=True)

    class Meta:
        abstract = True


class AWForm(LocalizedModel, PublicationModel):
    inputs = models.ManyToManyField(AWInput, related_name="aw_form_inputs")
    textarea = models.ForeignKey(
        AWTextArea, on_delete=models.SET_NULL, null=True, blank=True
    )
    disclaimer = models.ForeignKey(
        AWInput, on_delete=models.SET_NULL, null=True, blank=True
    )
    button = LocalizedCharField(blank=True, null=True, required=False)
    description = LocalizedTextField(blank=True, null=True, required=False)

    class Meta:
        abstract = True


class AWSection(AWFragment):
    items = GenericRelation(AWItem)

    class Meta:
        abstract = True


@reversion.register(exclude=("published_version",))
class AWHero(AWFragment):
    content = LocalizedTextField(blank=True, null=True, required=False)
    image = models.ForeignKey(AWImage, blank=True, null=True, on_delete=models.SET_NULL)
    actions = GenericRelation(AWAction)


@reversion.register(exclude=("published_version",))
class AWFaq(AWSection):
    columns = IntegerField(default=2)
    pass


@reversion.register(exclude=("published_version",))
class AWCallToAction(LocalizedModel, PublicationModel):
    title = LocalizedTextField(blank=True, null=True, required=False)
    subtitle = LocalizedTextField(blank=True, null=True, required=False)
    actions = GenericRelation(AWAction)


class BlogPostsBase(LocalizedModel, PublicationModel):
    title = LocalizedTextField(blank=True, null=True, required=False)
    link_text = LocalizedCharField(blank=True, null=True, required=False)
    link_url = LocalizedCharField(blank=True, null=True, required=False)
    information = LocalizedTextField(blank=True, null=True, required=False)

    class Meta:
        abstract = True


@reversion.register(exclude=("published_version",))
class AWBlogHighlightedPost(BlogPostsBase):
    post_ids = ArrayField(IntegerField(), default=list, blank=True)


@reversion.register(exclude=("published_version",))
class AWBlogLatestPost(BlogPostsBase):
    count = IntegerField(default=0)


@reversion.register(exclude=("published_version",))
class AWBrand(AWFragment):
    images = models.ManyToManyField(AWImage, related_name="aw_brands")


@reversion.register(exclude=("published_version",))
class AWContact(AWFragment, AWForm):
    pass


@reversion.register(exclude=("published_version",))
class AWContent(AWSection, AWGenericBaseModel):
    limit = Q(app_label="astrowind_pages")

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=limit,
        blank=True,
        null=True,
    )

    object_id = models.PositiveIntegerField(blank=True, null=True)

    content = LocalizedTextField(blank=True, null=True, required=False)
    call_to_action = models.ForeignKey(
        AWAction, on_delete=models.SET_NULL, blank=True, null=True
    )
    columns = models.IntegerField()
    image = models.ForeignKey(AWImage, on_delete=models.SET_NULL, blank=True, null=True)
    is_reversed = models.BooleanField(default=False)
    is_after_content = models.BooleanField(default=False)

    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position"]


class AWBaseFeature(AWSection):
    columns = models.IntegerField(default=0)
    default_icon = models.CharField(default="", blank=True)

    class Meta:
        abstract = True


@reversion.register(exclude=("published_version",))
class AWFeature(AWBaseFeature):
    columns = models.IntegerField(default=2)


@reversion.register(exclude=("published_version",))
class AWFeature2(AWBaseFeature):
    columns = models.IntegerField(default=3)


@reversion.register(exclude=("published_version",))
class AWFeature3(AWBaseFeature):
    is_before_content = models.BooleanField(default=False)
    is_after_content = models.BooleanField(default=False)


class AWBaseLinkItem(LocalizedModel, PublicationModel):
    text = LocalizedCharField(blank=True, null=True, required=False)
    href = CharField(default="", blank=True)
    aria_label = LocalizedCharField(blank=True, null=True, required=False)
    icon = CharField(default="", blank=True)

    class Meta:
        abstract = True


@reversion.register(exclude=("published_version",))
class AWFooterLink(LocalizedModel, PublicationModel):
    pass


@reversion.register(exclude=("published_version",))
class AWFooterLinkItem(AWBaseLinkItem):
    footer_links = models.ForeignKey(
        AWFooterLink, on_delete=models.SET, null=True, blank=True
    )


@reversion.register(exclude=("published_version",))
class AWFooter(LocalizedModel, PublicationModel):
    links = models.ManyToManyField(AWFooterLink, related_name="links_footers")
    secondary_links = models.ManyToManyField(
        AWFooterLink, related_name="secondary_links_footers"
    )
    social_links = models.ManyToManyField(
        AWFooterLink, related_name="social_links_footers"
    )
    foot_name = LocalizedTextField(blank=True, null=True, required=False)


@reversion.register(exclude=("published_version",))
class AWHeroText(AWFragment):
    content = LocalizedTextField(blank=True, null=True, required=False)
    call_to_action = models.ForeignKey(
        AWCallToAction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cta_aw_hero_texts",
    )
    call_to_action2 = models.ForeignKey(
        AWCallToAction,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cta2_aw_hero_texts",
    )


@reversion.register(exclude=("published_version",))
class AWPricing(AWFragment):
    pass


@reversion.register(exclude=("published_version",))
class AWPriceItem(LocalizedModel, PublicationModel):
    title = LocalizedCharField(blank=True, null=True, required=False)
    subtitle = LocalizedCharField(blank=True, null=True, required=False)
    price = LocalizedCharField(blank=True, null=True, required=False)
    period = LocalizedCharField(blank=True, null=True, required=False)
    call_to_action = models.ForeignKey(
        AWCallToAction, on_delete=models.SET_NULL, null=True, blank=True
    )
    has_ribbon = models.BooleanField(default=False)
    ribbon_title = LocalizedCharField(blank=True, null=True, required=False)

    items = GenericRelation(AWItem)

    pricing = models.ForeignKey(
        AWPricing,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="prices",
    )


@reversion.register(exclude=("published_version",))
class AWStat(AWFragment):
    pass


@reversion.register(exclude=("published_version",))
class AWStatItem(LocalizedModel, PublicationModel):
    title = LocalizedCharField(blank=True, null=True, required=False)
    amount = LocalizedCharField(blank=True, null=True, required=False)
    icon = CharField(default="", blank=True)

    stat_group = models.ForeignKey(
        AWStat, on_delete=models.SET_NULL, null=True, blank=True, related_name="stats"
    )

    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position"]


@reversion.register(exclude=("published_version",))
class AWStep(AWSection):
    image = models.ForeignKey(AWImage, blank=True, null=True, on_delete=models.SET_NULL)
    is_reversed = models.BooleanField(default=False)


@reversion.register(exclude=("published_version",))
class AWStep2(AWSection):
    call_to_action = models.ForeignKey(
        AWCallToAction, blank=True, null=True, on_delete=models.SET_NULL
    )
    is_reversed = models.BooleanField(default=False)


@reversion.register(exclude=("published_version",))
class AWTestimonial(AWFragment):
    call_to_action = models.ForeignKey(
        AWCallToAction, blank=True, null=True, on_delete=models.SET_NULL
    )


@reversion.register(exclude=("published_version",))
class AWTestimonialItem(LocalizedModel, PublicationModel):
    title = LocalizedCharField(blank=True, null=True, required=False)
    testimonial = LocalizedCharField(blank=True, null=True, required=False)
    name = LocalizedCharField(blank=True, null=True, required=False)
    job = LocalizedCharField(blank=True, null=True, required=False)
    image = models.ForeignKey(AWImage, blank=True, null=True, on_delete=models.SET_NULL)

    testimonial_group = models.ForeignKey(
        AWTestimonial,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="testimonials",
    )
