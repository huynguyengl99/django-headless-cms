import reversion
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import CharField, IntegerField
from django.utils.translation import gettext_lazy as _
from localized_fields.fields import (
    LocalizedCharField,
    LocalizedTextField,
)

from headless_cms.fields import AutoLanguageUrlField
from headless_cms.models import (
    LocalizedDynamicFileModel,
    LocalizedPublicationModel,
    M2MSortedOrderThrough,
    SortableGenericBaseModel,
)


class AWImage(LocalizedDynamicFileModel):
    pass


class AWAction(LocalizedPublicationModel):
    class CTAVariants(models.TextChoices):
        PRIMARY = "primary", _("Primary")
        SECONDARY = "secondary", _("Secondary")
        TERTIARY = "tertiary", _("Tertiary")
        LINK = "link", _("Link")

    variant = models.CharField(
        choices=CTAVariants.choices, default=CTAVariants.SECONDARY
    )
    target = models.CharField(default="", blank=True)
    text = LocalizedCharField(blank=True, null=True, required=False)
    href = AutoLanguageUrlField(default="", blank=True)
    icon = CharField(default="", blank=True)


@reversion.register(exclude=("published_version",))
class AWItem(SortableGenericBaseModel):
    title = LocalizedTextField(blank=True, null=True, required=False)
    description = LocalizedTextField(blank=True, null=True, required=False)
    icon = models.CharField(blank=True, default="")


class AWBaseInput(LocalizedPublicationModel):
    type = CharField(default="text", blank=True)
    name = CharField()
    label = LocalizedCharField(blank=True, null=True, required=False)
    autocomplete = CharField(default="on", blank=True)
    placeholder = LocalizedCharField(blank=True, null=True, required=False)

    class Meta:
        abstract = True


@reversion.register(exclude=("published_version",))
class AWInput(SortableGenericBaseModel, AWBaseInput):
    pass


@reversion.register(exclude=("published_version",))
class AWDisclaimer(LocalizedPublicationModel):
    label = LocalizedCharField(blank=True, null=True, required=False)


@reversion.register(exclude=("published_version",))
class AWTextArea(LocalizedPublicationModel):
    name = CharField(default="message")
    label = LocalizedCharField(blank=True, null=True, required=False)
    rows = IntegerField(default=4)
    placeholder = LocalizedCharField(blank=True, null=True, required=False)


class AWFragment(LocalizedPublicationModel):
    title = LocalizedTextField(blank=True, null=True, required=False)
    subtitle = LocalizedTextField(blank=True, null=True, required=False)
    tagline = LocalizedTextField(blank=True, null=True, required=False)
    html_id = models.CharField(default="", blank=True)

    class Meta:
        abstract = True


@reversion.register(exclude=("published_version",))
class AWForm(LocalizedPublicationModel):
    inputs = GenericRelation(AWInput)
    textarea = models.ForeignKey(
        AWTextArea, on_delete=models.SET_NULL, null=True, blank=True
    )
    disclaimer = models.ForeignKey(
        AWDisclaimer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    button = LocalizedCharField(blank=True, null=True, required=False)
    description = LocalizedTextField(blank=True, null=True, required=False)
    submit_url = LocalizedCharField(default=dict, blank=True, null=True, required=False)

    class Meta:
        abstract = True


class AWSection(AWFragment):
    items = GenericRelation(AWItem)

    class Meta:
        abstract = True


@reversion.register(exclude=("published_version",))
class AWHero(AWFragment):
    content = LocalizedTextField(blank=True, null=True, required=False)

    image = models.ForeignKey(
        AWImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="aw_heroes",
    )
    actions = models.ManyToManyField(
        AWAction,
        related_name="heroes",
        blank=True,
        through="AWHeroActionThrough",
    )


class AWHeroActionThrough(M2MSortedOrderThrough):
    hero = models.ForeignKey(AWHero, on_delete=models.CASCADE)
    action = models.ForeignKey(AWAction, on_delete=models.CASCADE)


@reversion.register(exclude=("published_version",))
class AWFaq(AWSection):
    columns = IntegerField(default=2)
    pass


@reversion.register(exclude=("published_version",))
class AWCallToAction(LocalizedPublicationModel):
    title = LocalizedTextField(blank=True, null=True, required=False)
    subtitle = LocalizedTextField(blank=True, null=True, required=False)
    tagline = LocalizedTextField(blank=True, null=True, required=False)
    actions = models.ManyToManyField(
        AWAction,
        related_name="ctas",
        blank=True,
        through="AWCTAActionThrough",
    )


class AWCTAActionThrough(M2MSortedOrderThrough):
    cta = models.ForeignKey(AWCallToAction, on_delete=models.CASCADE)
    action = models.ForeignKey(AWAction, on_delete=models.CASCADE)


class BlogPostsBase(LocalizedPublicationModel):
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
    images = models.ManyToManyField(
        AWImage,
        related_name="brands",
        blank=True,
        through="AWBrandImageThrough",
    )


class AWBrandImageThrough(M2MSortedOrderThrough):
    brand = models.ForeignKey(AWBrand, on_delete=models.CASCADE)
    image = models.ForeignKey(AWImage, on_delete=models.CASCADE)


@reversion.register(exclude=("published_version",))
class AWContact(AWFragment, AWForm):
    pass


@reversion.register(exclude=("published_version",))
class AWContent(AWSection):
    call_to_action = models.ForeignKey(
        AWAction,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="aw_contents",
    )
    image = models.ForeignKey(
        AWImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="aw_contents",
    )

    content = LocalizedTextField(blank=True, null=True, required=False)
    columns = models.IntegerField()
    is_reversed = models.BooleanField(default=False)
    is_after_content = models.BooleanField(default=False)

    items = GenericRelation(AWItem)


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


class AWBaseLinkItem(LocalizedPublicationModel):
    text = LocalizedCharField(blank=True, null=True, required=False)
    href = AutoLanguageUrlField(default="", blank=True)
    aria_label = LocalizedCharField(blank=True, null=True, required=False)
    icon = CharField(default="", blank=True)

    class Meta:
        abstract = True


@reversion.register(exclude=("published_version",))
class AWHeaderLink(AWBaseLinkItem):
    links = models.ManyToManyField(
        "self", through="AWHeaderLinkSelfThrough", symmetrical=False
    )


class AWHeaderLinkSelfThrough(M2MSortedOrderThrough):
    parent_link = models.ForeignKey(
        AWHeaderLink, on_delete=models.CASCADE, related_name="link_parents"
    )
    child_link = models.ForeignKey(
        AWHeaderLink, on_delete=models.CASCADE, related_name="link_children"
    )


@reversion.register(exclude=("published_version",))
class AWHeader(LocalizedPublicationModel):
    links = models.ManyToManyField(
        AWHeaderLink,
        related_name="links_headers",
        blank=True,
        through="AWHeaderLinkThrough",
    )
    actions = models.ManyToManyField(
        AWAction,
        related_name="actions_headers",
        blank=True,
        through="AWHeaderActionThrough",
    )


class AWHeaderLinkThrough(M2MSortedOrderThrough):
    header = models.ForeignKey(AWHeader, on_delete=models.CASCADE)
    header_link = models.ForeignKey(AWHeaderLink, on_delete=models.CASCADE)


class AWHeaderActionThrough(M2MSortedOrderThrough):
    header = models.ForeignKey(AWHeader, on_delete=models.CASCADE)
    action = models.ForeignKey(AWAction, on_delete=models.CASCADE)


@reversion.register(exclude=("published_version",))
class AWFooterLink(LocalizedPublicationModel):
    title = LocalizedTextField(default=dict, blank=True, null=True, required=False)
    links = models.ManyToManyField(
        "AWFooterLinkItem",
        through="AWFooterLinkThrough",
        related_name="links_footers",
        blank=True,
    )


@reversion.register(exclude=("published_version",))
class AWFooterLinkItem(AWBaseLinkItem):
    pass


class AWFooterLinkThrough(M2MSortedOrderThrough):
    footer_link = models.ForeignKey(AWFooterLink, on_delete=models.CASCADE)
    footer_link_item = models.ForeignKey(AWFooterLinkItem, on_delete=models.CASCADE)


@reversion.register(exclude=("published_version",))
class AWFooter(LocalizedPublicationModel):
    links = models.ManyToManyField(
        AWFooterLink,
        related_name="links_footers",
        blank=True,
        through="AWFooterLinksThrough",
    )
    secondary_links = models.ManyToManyField(
        AWFooterLink,
        related_name="secondary_links_footers",
        blank=True,
        through="AWFooterSecondaryLinksThrough",
    )
    social_links = models.ManyToManyField(
        AWFooterLink,
        related_name="social_links_footers",
        blank=True,
        through="AWFooterSocialLinksThrough",
    )
    foot_note = LocalizedTextField(blank=True, null=True, required=False)


class AWFooterLinkBaseThough(M2MSortedOrderThrough):
    footer = models.ForeignKey(AWFooter, on_delete=models.CASCADE)
    footer_link = models.ForeignKey(AWFooterLink, on_delete=models.CASCADE)

    class Meta(M2MSortedOrderThrough.Meta):
        abstract = True


class AWFooterLinksThrough(AWFooterLinkBaseThough):
    pass


class AWFooterSecondaryLinksThrough(AWFooterLinkBaseThough):
    pass


class AWFooterSocialLinksThrough(AWFooterLinkBaseThough):
    pass


@reversion.register(exclude=("published_version",))
class AWHeroText(AWFragment):
    content = LocalizedTextField(blank=True, null=True, required=False)
    call_to_action = models.ForeignKey(
        AWAction,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="aw_cta1_hero_texts",
    )
    call_to_action2 = models.ForeignKey(
        AWAction,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="aw_cta2_hero_texts",
    )


@reversion.register(exclude=("published_version",))
class AWPriceItem(LocalizedPublicationModel):
    title = LocalizedCharField(blank=True, null=True, required=False)
    subtitle = LocalizedCharField(blank=True, null=True, required=False)
    price = LocalizedCharField(blank=True, null=True, required=False)
    period = LocalizedCharField(blank=True, null=True, required=False)
    has_ribbon = models.BooleanField(default=False)
    ribbon_title = LocalizedCharField(blank=True, null=True, required=False)

    call_to_action = models.ForeignKey(
        AWAction,
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        related_name="price_items",
    )

    items = GenericRelation(AWItem)


@reversion.register(exclude=("published_version",))
class AWPricing(AWFragment):
    prices = models.ManyToManyField(
        AWPriceItem,
        related_name="aw_pricing",
        blank=True,
        through="AWPriceItemThrough",
    )


class AWPriceItemThrough(M2MSortedOrderThrough):
    pricing = models.ForeignKey(AWPricing, on_delete=models.CASCADE)
    price_item = models.ForeignKey(AWPriceItem, on_delete=models.CASCADE)


@reversion.register(exclude=("published_version",))
class AWStat(AWFragment):
    stats = models.ManyToManyField(
        "AWStatItem",
        related_name="stat_groups",
        blank=True,
        through="AWStatItemThrough",
    )


@reversion.register(exclude=("published_version",))
class AWStatItem(LocalizedPublicationModel):
    title = LocalizedCharField(blank=True, null=True, required=False)
    amount = LocalizedCharField(blank=True, null=True, required=False)
    icon = CharField(default="", blank=True)


class AWStatItemThrough(M2MSortedOrderThrough):
    stat = models.ForeignKey(AWStat, on_delete=models.CASCADE)
    stat_item = models.ForeignKey(AWStatItem, on_delete=models.CASCADE)


@reversion.register(exclude=("published_version",))
class AWStep(AWSection):
    is_reversed = models.BooleanField(default=False)
    image = models.ForeignKey(
        AWImage,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="steps",
    )


@reversion.register(exclude=("published_version",))
class AWStep2(AWSection):
    is_reversed = models.BooleanField(default=False)
    call_to_action = models.ForeignKey(
        AWAction,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="step2s",
    )


@reversion.register(exclude=("published_version",))
class AWTestimonial(AWFragment):
    call_to_action = models.ForeignKey(
        AWAction,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="testimonials",
    )


@reversion.register(exclude=("published_version",))
class AWTestimonialItem(LocalizedPublicationModel):
    title = LocalizedCharField(blank=True, null=True, required=False)
    testimonial = LocalizedCharField(blank=True, null=True, required=False)
    name = LocalizedCharField(blank=True, null=True, required=False)
    job = LocalizedCharField(blank=True, null=True, required=False)

    image = models.ForeignKey(
        AWImage,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="testimonial_items",
    )

    testimonial_group = models.ForeignKey(
        AWTestimonial,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="testimonials",
    )

    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position"]
