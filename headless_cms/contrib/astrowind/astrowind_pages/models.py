import reversion
from django.db import models
from localized_fields.fields import LocalizedTextField

from headless_cms.contrib.astrowind.astrowind_widgets.models import (
    AWCallToAction,
    AWContact,
    AWContent,
    AWFaq,
    AWFeature,
    AWFeature2,
    AWFeature3,
    AWFooter,
    AWHeader,
    AWHero,
    AWHeroText,
    AWPricing,
    AWStat,
    AWStep,
    AWStep2,
)
from headless_cms.models import (
    LocalizedPublicationModel,
    LocalizedSingletonModel,
    M2MSortedOrderThrough,
)


@reversion.register(exclude=("published_version",))
class AWIndexPage(LocalizedPublicationModel, LocalizedSingletonModel):
    title = LocalizedTextField(default=dict, blank=True, null=True)

    hero = models.ForeignKey(AWHero, blank=True, null=True, on_delete=models.SET_NULL)
    feature = models.ForeignKey(
        AWFeature, blank=True, null=True, on_delete=models.SET_NULL
    )
    feature2 = models.ForeignKey(
        AWFeature2, blank=True, null=True, on_delete=models.SET_NULL
    )
    step = models.ForeignKey(AWStep, blank=True, null=True, on_delete=models.SET_NULL)

    contents = models.ManyToManyField(
        AWContent,
        related_name="index_page",
        blank=True,
        through="AWIndexPageContentThrough",
    )

    faq = models.ForeignKey(AWFaq, blank=True, null=True, on_delete=models.SET_NULL)
    stat = models.ForeignKey(AWStat, blank=True, null=True, on_delete=models.SET_NULL)
    cta = models.ForeignKey(
        AWCallToAction, blank=True, null=True, on_delete=models.SET_NULL
    )


class AWIndexPageContentThrough(M2MSortedOrderThrough):
    index_page = models.ForeignKey(AWIndexPage, on_delete=models.SET_NULL, null=True)
    content = models.ForeignKey(AWContent, on_delete=models.SET_NULL, null=True)


@reversion.register(exclude=("published_version",))
class AWSite(LocalizedPublicationModel, LocalizedSingletonModel):
    header = models.ForeignKey(
        AWHeader, blank=True, null=True, on_delete=models.SET_NULL
    )
    footer = models.ForeignKey(
        AWFooter, blank=True, null=True, on_delete=models.SET_NULL
    )


class AWAboutFeature3Through(M2MSortedOrderThrough):
    about_page = models.ForeignKey("AWAboutPage", on_delete=models.SET_NULL, null=True)
    feature3 = models.ForeignKey(AWFeature3, on_delete=models.SET_NULL, null=True)


class AWAboutFeature2Through(M2MSortedOrderThrough):
    about_page = models.ForeignKey("AWAboutPage", on_delete=models.SET_NULL, null=True)
    feature2 = models.ForeignKey(AWFeature2, on_delete=models.SET_NULL, null=True)


class AWAboutStep2Through(M2MSortedOrderThrough):
    about_page = models.ForeignKey("AWAboutPage", on_delete=models.SET_NULL, null=True)
    step2 = models.ForeignKey(AWStep2, on_delete=models.SET_NULL, null=True)


@reversion.register(exclude=("published_version",))
class AWAboutPage(LocalizedPublicationModel, LocalizedSingletonModel):
    title = LocalizedTextField(default=dict, blank=True, null=True)

    hero = models.ForeignKey(AWHero, blank=True, null=True, on_delete=models.SET_NULL)
    stat = models.ForeignKey(AWStat, blank=True, null=True, on_delete=models.SET_NULL)

    feature3s = models.ManyToManyField(
        AWFeature3, blank=True, through=AWAboutFeature3Through
    )
    step2s = models.ManyToManyField(AWStep2, blank=True, through=AWAboutStep2Through)

    feature2s = models.ManyToManyField(
        AWFeature2, blank=True, through=AWAboutFeature2Through
    )


@reversion.register(exclude=("published_version",))
class AWPricingPage(LocalizedPublicationModel, LocalizedSingletonModel):
    title = LocalizedTextField(default=dict, blank=True, null=True)

    hero_text = models.ForeignKey(
        AWHeroText, blank=True, null=True, on_delete=models.SET_NULL
    )
    prices = models.ForeignKey(
        AWPricing, blank=True, null=True, on_delete=models.SET_NULL
    )
    feature3 = models.ForeignKey(
        AWFeature3, blank=True, null=True, on_delete=models.SET_NULL
    )
    step = models.ForeignKey(AWStep, blank=True, null=True, on_delete=models.SET_NULL)
    faq = models.ForeignKey(AWFaq, blank=True, null=True, on_delete=models.SET_NULL)
    cta = models.ForeignKey(
        AWCallToAction, blank=True, null=True, on_delete=models.SET_NULL
    )


@reversion.register(exclude=("published_version",))
class AWContactPage(LocalizedPublicationModel, LocalizedSingletonModel):
    title = LocalizedTextField(default=dict, blank=True, null=True)

    hero_text = models.ForeignKey(
        AWHeroText, blank=True, null=True, on_delete=models.SET_NULL
    )
    contact_us = models.ForeignKey(
        AWContact, blank=True, null=True, on_delete=models.SET_NULL
    )
    feature2 = models.ForeignKey(
        AWFeature2, blank=True, null=True, on_delete=models.SET_NULL
    )
