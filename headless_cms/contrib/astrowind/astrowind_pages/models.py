import reversion
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from solo.models import SingletonModel

from headless_cms.contrib.astrowind.astrowind_widgets.models import (
    AWCallToAction,
    AWContent,
    AWFaq,
    AWFeature,
    AWFeature2,
    AWHero,
    AWStat,
    AWStep,
)
from headless_cms.models import LocalizedPublicationModel


@reversion.register(exclude=("published_version",))
class AWIndexPage(LocalizedPublicationModel, SingletonModel):
    hero = models.ForeignKey(AWHero, blank=True, null=True, on_delete=models.SET_NULL)
    feature = models.ForeignKey(
        AWFeature, blank=True, null=True, on_delete=models.SET_NULL
    )
    feature2 = models.ForeignKey(
        AWFeature2, blank=True, null=True, on_delete=models.SET_NULL
    )
    step = models.ForeignKey(AWStep, blank=True, null=True, on_delete=models.SET_NULL)

    contents = GenericRelation(AWContent)

    faq = models.ForeignKey(AWFaq, blank=True, null=True, on_delete=models.SET_NULL)
    stat = models.ForeignKey(AWStat, blank=True, null=True, on_delete=models.SET_NULL)
    cta = models.ForeignKey(
        AWCallToAction, blank=True, null=True, on_delete=models.SET_NULL
    )

    @classmethod
    def get_solo(cls):
        obj: AWIndexPage = super().get_solo()
        if not obj.published_version_id:
            return None
        return obj
