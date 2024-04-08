import reversion
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from solo import settings as solo_settings
from solo.models import SingletonModel, get_cache

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
        cache_name = getattr(settings, "SOLO_CACHE", solo_settings.SOLO_CACHE)
        if not cache_name:
            obj, created = cls.published_objects.published().get_or_create(
                pk=cls.singleton_instance_id
            )
            return obj
        cache = get_cache(cache_name)
        cache_key = cls.get_cache_key()
        obj = cache.get(cache_key)
        if not obj:
            obj, created = cls.published_objects.published().get_or_create(
                pk=cls.singleton_instance_id
            )
            obj.set_to_cache()
        return obj
