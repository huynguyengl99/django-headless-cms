from functools import cached_property

from django.contrib import admin
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Prefetch
from django.utils.html import format_html
from reversion.models import Version


class PublishedQuerySet(models.QuerySet):
    def serialize(self):
        return [p.published_version.field_dict for p in self.all()]

    serialize.queryset_only = True

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

    @admin.display
    def published_state(self):
        state = '<div style="color:red;">unpublished<div>'
        if self.published_version:
            last_ver = Version.objects.get_for_object(self).first()
            if last_ver.id == self.published_version.id:
                state = '<div style="color:blue;">published (latest)<div>'
            else:
                state = '<div style="color:orange;">published (outdated)<div>'

        return format_html(state)

    published_state.allow_tags = True
