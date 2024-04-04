import reversion
from django.conf import settings
from django.db import models
from localized_fields.models import LocalizedModel
from solo import settings as solo_settings
from solo.models import SingletonModel, get_cache

from headless_cms.contrib.astrowind.astrowind_widgets.models import (
    AWCallToAction,
    AWFaq,
    AWFeature,
    AWHero,
    AWStep,
)
from headless_cms.models import PublicationModel


@reversion.register(exclude=("published_version",))
class AWIndexPage(LocalizedModel, PublicationModel, SingletonModel):
    hero = models.ForeignKey(AWHero, blank=True, null=True, on_delete=models.SET_NULL)
    features = models.ForeignKey(
        AWFeature, blank=True, null=True, on_delete=models.SET_NULL
    )
    steps = models.ForeignKey(AWStep, blank=True, null=True, on_delete=models.SET_NULL)
    faqs = models.ForeignKey(AWFaq, blank=True, null=True, on_delete=models.SET_NULL)
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
