from functools import lru_cache
from urllib.parse import quote as urlquote

import reversion
from adminsortable2.admin import (
    SortableAdminBase,
    SortableGenericInlineAdminMixin,
    SortableStackedInline,
)
from django.contrib import admin, messages
from django.contrib.admin import StackedInline
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.admin.utils import unquote
from django.contrib.contenttypes.admin import GenericStackedInline
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import ManyToManyField
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.html import format_html
from django.utils.translation import gettext as _
from import_export.admin import ImportExportActionModelAdmin
from localized_fields.admin import LocalizedFieldsAdminMixin
from martor.widgets import AdminMartorWidget
from rest_framework import status
from reversion.admin import VersionAdmin
from reversion.models import Version
from solo.admin import SingletonModelAdmin

from headless_cms.models import (
    LocalizedPublicationModel,
    LocalizedSingletonModel,
    M2MSortedOrderThrough,
    PublicationModel,
    SortableGenericBaseModel,
)
from headless_cms.settings import headless_cms_settings
from headless_cms.utils.custom_import_export import override_modelresource_factory


class PublishStatusInlineMixin:
    show_change_link = True

    readonly_fields = ("publish_status",)

    def _get_publish_status(self, obj):
        published_state = "unpublished"
        if obj.published_version:
            last_ver = Version.objects.get_for_object(obj).first()
            if last_ver.id == obj.published_version.id:
                published_state = "published (latest)"
            else:
                published_state = "published (outdated)"
        return published_state

    def publish_status(self, obj):
        published_state = "unpublished"
        if hasattr(obj, "is_through_table") and obj.is_through_table:
            fields = obj._meta.get_fields()
            for field in fields:
                rel_model = field.related_model
                if not rel_model or not issubclass(rel_model, PublicationModel):
                    continue
                if self.fk_name:
                    if field.name == self.fk_name:
                        continue
                    else:
                        return self._get_publish_status(getattr(obj, field.name))
                elif rel_model != self.parent_model:
                    published_state = self._get_publish_status(getattr(obj, field.name))
        else:
            published_state = self._get_publish_status(obj)
        return published_state


class BaseGenericAdmin(
    PublishStatusInlineMixin,
    GenericStackedInline,
):
    extra = 0


class BaseSortableGenericAdmin(
    SortableGenericInlineAdminMixin,
    SortableStackedInline,
    BaseGenericAdmin,
):
    extra = 0


@admin.action(description="Publish selected")
def publish(modeladmin, request, queryset):
    for obj in queryset.all():
        obj.publish(request.user)


@admin.action(description="Unpublish selected")
def unpublish(modeladmin, request, queryset):
    for obj in queryset.all():
        obj.unpublish(request.user)


@admin.action(description="Translate untranslated contents")
def translate_missing(modeladmin, request, queryset):
    for obj in queryset.all():
        headless_cms_settings.AUTO_TRANSLATE_CLASS(obj, user=request.user).process()


@admin.action(description="Force translate (override old translation)")
def force_translate(modeladmin, request, queryset):
    for obj in queryset.all():
        headless_cms_settings.AUTO_TRANSLATE_CLASS(obj, user=request.user).process(
            force=True
        )


class EnhancedLocalizedVersionAdmin(
    ImportExportActionModelAdmin, LocalizedFieldsAdminMixin, VersionAdmin
):
    actions = [publish, unpublish, translate_missing, force_translate]
    formfield_overrides = {
        models.TextField: {"widget": AdminMartorWidget},
    }

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        return list_display + ("published_state",)

    def render_change_form(self, request, context, *args, **kwargs):
        """We need to update the context to show the button."""
        obj = kwargs.get("obj")
        if obj and not context.get("revert"):
            show_publish = True
            show_unpublish = False
            show_recursively_publish = any(
                f.is_relation
                and not f.auto_created
                and f.related_model
                and issubclass(f.related_model, LocalizedPublicationModel)
                for f in obj._meta.get_fields()
            )

            published_state = "unpublished"
            if obj.published_version:
                last_ver = Version.objects.get_for_object(obj).first()
                show_unpublish = True
                if last_ver.id == obj.published_version.id:
                    published_state = "published (latest)"
                    show_publish = False
                else:
                    published_state = "published (outdated)"

            context.update(
                {
                    "published_state": published_state,
                    "show_publish": show_publish,
                    "show_unpublish": show_unpublish,
                    "show_recursively_publish": show_recursively_publish,
                    "show_translate": True,
                }
            )

        return super().render_change_form(request, context, *args, **kwargs)

    def changelist_view(self, request, extra_context=None):
        if request.POST and "action" in request.POST:
            context = {
                "has_change_permission": self.has_change_permission(request),
            }
            context.update(extra_context or {})
            return super(VersionAdmin, self).changelist_view(request, context)
        else:
            return super().changelist_view(request, extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        res = super().change_view(request, object_id, form_url, extra_context)

        if "_publish" in request.POST:
            with reversion.create_revision(manage_manually=True):
                obj = self.get_object(request, unquote(object_id))
                last_ver = Version.objects.get_for_object(obj).first()

                obj.published_version = last_ver
                obj.save()
        elif "_unpublish" in request.POST:
            with reversion.create_revision(manage_manually=True):
                obj = self.get_object(request, unquote(object_id))
                obj.published_version = None
                obj.save()
        elif "_recursively_publish" in request.POST:
            obj = self.get_object(request, unquote(object_id))
            obj.recursively_publish(request.user)
        return res

    def response_change(self, request, obj):
        opts = self.opts
        preserved_filters = self.get_preserved_filters(request)

        msg_dict = {
            "name": opts.verbose_name,
            "obj": format_html('<a href="{}">{}</a>', urlquote(request.path), obj),
        }
        if "_publish" in request.POST:
            reversion.set_comment("Publish")

            msg = format_html(
                _("The {name} “{obj}” was published successfully."),
                **msg_dict,
            )
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = request.path
            redirect_url = add_preserved_filters(
                {"preserved_filters": preserved_filters, "opts": opts}, redirect_url
            )
            return HttpResponseRedirect(redirect_url)
        elif "_unpublish" in request.POST:
            reversion.set_comment("Unpublished")

            msg = format_html(
                _("The {name} “{obj}” was unpublished."),
                **msg_dict,
            )
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = request.path
            redirect_url = add_preserved_filters(
                {"preserved_filters": preserved_filters, "opts": opts}, redirect_url
            )
            return HttpResponseRedirect(redirect_url)
        elif "_translate" in request.POST or "_force_translate" in request.POST:
            force = "_force_translate" in request.POST

            translator = headless_cms_settings.AUTO_TRANSLATE_CLASS(
                obj, user=request.user
            )
            translator.process(force=force)

            msg = format_html(
                _(
                    f"The {{name}} “{{obj}}” was translated{' (forced)' if force else ''}."
                ),
                **msg_dict,
            )
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = request.path
            redirect_url = add_preserved_filters(
                {"preserved_filters": preserved_filters, "opts": opts}, redirect_url
            )
            return HttpResponseRedirect(redirect_url)
        else:
            # Otherwise, use default behavior
            return super().response_change(request, obj)

    def revision_view(self, request, object_id, version_id, extra_context=None):
        """Displays the contents of the given revision."""
        object_id = unquote(object_id)  # Underscores in primary key get quoted to "_5F"
        version = get_object_or_404(Version, pk=version_id, object_id=object_id)
        context = {
            "title": _("Revert %(name)s") % {"name": version.object_repr},
            "revert": True,
            "is_published": (
                version.object.published_version
                and version.revision_id == version.object.published_version.revision_id
            ),
        }
        context.update(extra_context or {})
        return self._reversion_revisionform_view(
            request,
            version,
            self.revision_form_template
            or self._reversion_get_template_list("revision_form.html"),
            context,
        )

    def _reversion_revisionform_view(
        self, request, version, template_name, extra_context=None
    ):
        old_published_version = (
            version.object.published_version if version.object else None
        )
        res = super()._reversion_revisionform_view(
            request, version, template_name, extra_context
        )

        if res.status_code == status.HTTP_302_FOUND:
            if old_published_version:
                with reversion.create_revision(manage_manually=True):
                    version.refresh_from_db()
                    version.object.published_version_id = old_published_version
                    version.object.save()

        return res

    def get_resource_classes(self):
        if not self.resource_classes and not self.resource_class:
            return [override_modelresource_factory(self.model)]
        return super().get_resource_classes()


@lru_cache(maxsize=0)
def create_m2m_inline_admin(model, sortable=False):
    return type(
        model.__name__ + "Inline",
        (
            PublishStatusInlineMixin,
            SortableStackedInline if sortable else StackedInline,
        ),
        {"extra": 0, "model": model},
    )


@lru_cache(maxsize=0)
def create_generic_inline_admin(model, sortable=False):
    return type(
        model.__name__ + "Inline",
        (BaseSortableGenericAdmin if sortable else BaseGenericAdmin,),
        {"model": model},
    )


def auto_admins(
    model_list: list[type[models.Model]],
):
    for model in model_list:
        admin_attrs = {"history_latest_first": True}
        inlines = []
        exclude = []
        model_fields = model._meta.get_fields()
        has_sortable_base = False
        for field in model_fields:
            if isinstance(field, ManyToManyField) and issubclass(
                field.related_model, LocalizedPublicationModel
            ):
                through = getattr(model, field.name).through
                exclude.append(field.name)

                can_sort = False
                if issubclass(through, M2MSortedOrderThrough):
                    can_sort = True
                    has_sortable_base = True

                inlines.append(create_m2m_inline_admin(through, can_sort))
            elif isinstance(field, GenericRelation) and issubclass(
                field.related_model, LocalizedPublicationModel
            ):
                can_sort = False
                has_sortable_base = True

                if issubclass(field.related_model, SortableGenericBaseModel):
                    can_sort = True

                inlines.append(
                    create_generic_inline_admin(field.related_model, can_sort)
                )

        admin_attrs["inlines"] = inlines
        admin_attrs["exclude"] = exclude

        base_admin = []
        if has_sortable_base:
            base_admin = [SortableAdminBase]

        base_admin.append(EnhancedLocalizedVersionAdmin)

        if issubclass(model, LocalizedSingletonModel):
            base_admin.append(SingletonModelAdmin)

        admin_model = type(model.__name__ + "Admin", tuple(base_admin), admin_attrs)
        admin.site.register(model, admin_model)
