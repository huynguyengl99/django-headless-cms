from functools import cached_property

import reversion
from django.contrib import admin
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.html import format_html
from localized_fields.fields import (
    LocalizedCharField,
    LocalizedFileField,
    LocalizedTextField,
)
from localized_fields.models import LocalizedModel
from reversion.models import Version
from solo.models import SingletonModel

from headless_cms.fields.slug_field import LocalizedUniqueNormalizedSlugField
from headless_cms.settings import headless_cms_settings


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


class LocalizedPublicationModel(LocalizedModel):
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

    class Meta(LocalizedModel.Meta):
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

    def recursive_action(self, action, *args, **kwargs):
        action(self, *args, **kwargs)

        for f in self._meta.get_fields():
            if (
                f.is_relation
                and not f.auto_created
                and f.related_model
                and issubclass(f.related_model, LocalizedPublicationModel)
            ):
                if f.many_to_one:
                    rel_obj = getattr(self, f.name)
                    if rel_obj:
                        rel_obj.recursive_action(action, *args, **kwargs)
                elif f.many_to_many or f.one_to_many:
                    rel_objs = getattr(self, f.name).all()
                    for rel_obj in rel_objs:
                        rel_obj.recursive_action(action, *args, **kwargs)

    def recursively_publish(self, user=None):
        self.recursive_action(self.__class__.publish, user)

    def unpublish(self, user=None):
        with reversion.create_revision():
            reversion.set_comment("Unpublish")
            if user:
                reversion.set_user(user)

            self.save()

        with reversion.create_revision(manage_manually=True):
            self.published_version = None
            self.save()

    def translate(self, user=None, force=False):
        with reversion.create_revision():
            reversion.set_comment(f"Object translated{' (forced)' if force else ''}.")

            if user:
                reversion.set_user(user)
            translator = headless_cms_settings.AUTO_TRANSLATE_CLASS(self)
            translator.process(force=force)

    def recursively_translate(self, user=None, force=False):
        self.recursive_action(self.__class__.translate, user, force=force)

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


class LocalizedDynamicFileModel(LocalizedPublicationModel):
    src_file = LocalizedFileField(default=dict, blank=True, null=True, required=False)
    src_url = LocalizedCharField(default=dict, blank=True, null=True, required=False)
    alt = LocalizedTextField(blank=True, null=True, required=False)

    class Meta:
        abstract = True

    @property
    def src_link(self):
        src_file = self.src_file.translate()
        if src_file:
            src_url = src_file.url
            if src_url.startswith("/"):
                src_url = f"{headless_cms_settings.CMS_HOST}{src_url}"
            return src_url
        elif self.src_url:
            return self.src_url.translate()


class SortableGenericBaseModel(LocalizedPublicationModel):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    object = GenericForeignKey(
        ct_field="content_type",
        fk_field="object_id",
    )

    object_id = models.PositiveIntegerField(blank=True, null=True)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position"]
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
