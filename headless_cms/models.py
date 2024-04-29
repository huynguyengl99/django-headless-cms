from functools import cached_property

import reversion
from django.contrib import admin
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.html import format_html
from localized_fields.fields import LocalizedTextField
from localized_fields.models import LocalizedModel
from reversion.models import Version
from solo.models import SingletonModel

from headless_cms.fields.slug_field import LocalizedUniqueNormalizedSlugField


class M2MSortedOrderThrough(models.Model):
    is_through_table = True
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position"]
        abstract = True


class PublishedQuerySet(models.QuerySet):
    @cached_property
    def prefetch_relation_list(self):
        from headless_cms.utils.relations import calculate_prefetch_relation  # noqa

        return calculate_prefetch_relation(self.model)

    def published(self, auto_prefetch=False):
        prefetches = []
        selects = []
        if auto_prefetch:
            prefetches, selects = self.prefetch_relation_list

        return (
            self.select_related(*selects)
            .prefetch_related(*prefetches)
            .filter(published_version__isnull=False)
        )


class PublishedManager(models.Manager):
    def get_queryset(self):
        return PublishedQuerySet(self.model, using=self._db)

    def published(self, auto_prefetch=False):
        return self.get_queryset().published(auto_prefetch)


class PublicationModel(models.Model):
    class AdminPublishedStateHtml:
        UNPUBLISHED = '<div style="color:red;">unpublished<div>'
        PUBLISHED_OUTDATED = '<div style="color:orange;">published (outdated)<div>'
        PUBLISHED_LATEST = '<div style="color:blue;">published (latest)<div>'

    published_version = models.ForeignKey(
        Version, editable=False, null=True, on_delete=models.SET_NULL
    )
    versions = GenericRelation(Version)

    objects = models.Manager()
    published_objects = PublishedManager()

    class Meta:
        abstract = True

    @property
    def published_data(self):
        if self.published_version_id:
            return self.published_version.field_dict

    def publish(self, user=None):
        with reversion.create_revision():
            reversion.set_comment("Publish")
            if user:
                reversion.set_user(user)

            self.save()

        with reversion.create_revision(manage_manually=True):
            last_ver = Version.objects.get_for_object(self).first()

            self.published_version = last_ver
            self.save()

    def unpublish(self, user=None):
        with reversion.create_revision():
            reversion.set_comment("Unpublish")
            if user:
                reversion.set_user(user)

            self.save()

        with reversion.create_revision(manage_manually=True):
            self.published_version = None
            self.save()

    @admin.display
    def published_state(self):
        state = self.AdminPublishedStateHtml.UNPUBLISHED
        if self.published_version_id:
            last_ver = Version.objects.get_for_object(self).first()
            if last_ver.id == self.published_version_id:
                state = self.AdminPublishedStateHtml.PUBLISHED_LATEST
            else:
                state = self.AdminPublishedStateHtml.PUBLISHED_OUTDATED

        return format_html(state)

    published_state.allow_tags = True


class LocalizedPublicationModel(LocalizedModel, PublicationModel):
    class Meta:
        abstract = True


class LocalizedSingletonModel(SingletonModel):
    @classmethod
    def get_solo(cls):
        obj = super().get_solo()
        if not obj.published_version_id:
            return None
        return obj

    class Meta:
        abstract = True


class LocalizedTitleSlugModel(LocalizedPublicationModel):
    title = LocalizedTextField(blank=True, null=True, required=False)
    slug = LocalizedUniqueNormalizedSlugField(
        populate_from="title", blank=True, null=True, required=False
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        abstract = True
