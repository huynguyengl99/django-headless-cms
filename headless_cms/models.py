from functools import cached_property

import reversion
from django.contrib import admin
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Prefetch
from django.utils.html import format_html
from polymorphic.managers import PolymorphicManager
from polymorphic.models import PolymorphicModel
from psqlextra.manager import PostgresManager
from reversion.models import Version


class PublishedQuerySet(models.QuerySet):
    @cached_property
    def prefetch_related_list(self):
        prefetch_list = set()
        related_fields = [
            f
            for f in self.model._meta.get_fields()
            if f.auto_created and not f.concrete
        ]
        for field in related_fields:
            if issubclass(field.model, PublicationModel) and field.related_name:
                prefetch_list.add(
                    Prefetch(
                        field.related_name,
                        queryset=field.related_model.published_objects.published(),
                    )
                )
        return prefetch_list

    def published(self):
        return self.prefetch_related(*self.prefetch_related_list).filter(
            published_version__isnull=False
        )


class PublishedManager(models.Manager):
    def get_queryset(self):
        return PublishedQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


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


class LocalizedPolymorphicManager(PostgresManager, PolymorphicManager):
    pass


class LocalizedPolymorphicModel(PolymorphicModel):
    objects = LocalizedPolymorphicManager()

    class Meta:
        abstract = True
        base_manager_name = "objects"
