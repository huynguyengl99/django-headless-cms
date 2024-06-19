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

from headless_cms.fields import LocalizedUniqueNormalizedSlugField
from headless_cms.models import (
    LocalizedPublicationModel,
    LocalizedSingletonModel,
    M2MSortedOrderThrough,
    SortableGenericBaseModel,
)
from headless_cms.utils.custom_import_export import override_modelresource_factory


class PublishStatusInlineMixin:
    """
    Mixin to show the publish status of related objects in inline admin.
    """

    readonly_fields = ("publish_status",)

    def _get_publish_status(self, obj):
        """
        Get the publish status of an object.

        Args:
            obj (models.Model): The object to check.

        Returns:
            str: The publish status.
        """
        published_state = "unpublished"
        if obj.published_version:
            last_ver = Version.objects.get_for_object(obj).first()
            if last_ver.id == obj.published_version.id:
                published_state = "published (latest)"
            else:
                published_state = "published (outdated)"
        return published_state

    def publish_status(self, obj):
        """
        Get the publish status of an object for display in the admin.

        Args:
            obj (models.Model): The object to check.

        Returns:
            str: The publish status.
        """
        published_state = "unpublished"
        if isinstance(obj, M2MSortedOrderThrough):
            fields = obj._meta.get_fields()
            for field in fields:
                rel_model = field.related_model
                if not rel_model or not issubclass(
                    rel_model, LocalizedPublicationModel
                ):
                    continue
                if self.fk_name:
                    if field.name == self.fk_name:
                        continue
                    else:
                        return self._get_publish_status(getattr(obj, field.name))
                elif rel_model != self.parent_model:
                    published_state = self._get_publish_status(getattr(obj, field.name))
        elif obj._meta.auto_created:
            parent_model = obj._meta.auto_created
            fields = obj._meta.get_fields()
            for field in fields:
                rel_model = field.related_model
                if not rel_model or not issubclass(
                    rel_model, LocalizedPublicationModel
                ):
                    continue
                if field.related_model != parent_model:
                    return self._get_publish_status(getattr(obj, field.name))
        else:
            published_state = self._get_publish_status(obj)
        return published_state


class BaseGenericAdmin(
    PublishStatusInlineMixin,
    GenericStackedInline,
):
    """
    Base class for generic inlines with publish status.
    """

    extra = 0


class BaseSortableGenericAdmin(
    SortableGenericInlineAdminMixin,
    SortableStackedInline,
    BaseGenericAdmin,
):
    """
    Base class for sortable generic inlines with publish status.
    """

    extra = 0


@admin.action(description="Publish selected")
def publish(modeladmin, request, queryset):
    """
    Admin action to publish selected objects.

    Args:
        modeladmin (ModelAdmin): The model admin.
        request (HttpRequest): The request object.
        queryset (QuerySet): The selected objects.
    """
    obj: LocalizedPublicationModel

    for obj in queryset.all():
        obj.publish(request.user)


@admin.action(description="Unpublish selected")
def unpublish(modeladmin, request, queryset):
    """
    Admin action to unpublish selected objects.

    Args:
        modeladmin (ModelAdmin): The model admin.
        request (HttpRequest): The request object.
        queryset (QuerySet): The selected objects.
    """
    obj: LocalizedPublicationModel

    for obj in queryset.all():
        obj.unpublish(request.user)


@admin.action(description="Translate untranslated contents")
def translate_missing(modeladmin, request, queryset):
    """
    Admin action to translate missing content for selected objects.

    Args:
        modeladmin (ModelAdmin): The model admin.
        request (HttpRequest): The request object.
        queryset (QuerySet): The selected objects.
    """
    obj: LocalizedPublicationModel

    for obj in queryset.all():
        obj.translate(request.user)


@admin.action(description="Force translate (override old translation)")
def force_translate(modeladmin, request, queryset):
    """
    Admin action to force translate selected objects, overriding old translations.

    Args:
        modeladmin (ModelAdmin): The model admin.
        request (HttpRequest): The request object.
        queryset (QuerySet): The selected objects.
    """
    obj: LocalizedPublicationModel

    for obj in queryset.all():
        obj.translate(request.user, force=True)


FORCE_TRANSLATE = {"_force_translate", "_recursively_force_translate"}
RECURSIVELY_TRANSLATE = {"_recursively_translate", "_recursively_force_translate"}
TRANSLATE_ACTIONS = {"_translate"} | FORCE_TRANSLATE | RECURSIVELY_TRANSLATE

PUBLISH_ACTIONS = {"_publish", "_unpublish", "_recursively_publish"}

HEADLESS_CMS_ACTIONS = PUBLISH_ACTIONS | TRANSLATE_ACTIONS


class EnhancedLocalizedVersionAdmin(
    ImportExportActionModelAdmin, LocalizedFieldsAdminMixin, VersionAdmin
):
    """
    Enhanced admin class for localized versioned models.

    Includes support for import/export, localization, and versioning.
    """

    actions = [publish, unpublish, translate_missing, force_translate]
    formfield_overrides = {
        models.TextField: {"widget": AdminMartorWidget},
    }

    def get_list_display(self, request):
        """
        Get the list display fields for the admin changelist.

        Args:
            request (HttpRequest): The request object.

        Returns:
            tuple: The list display fields.
        """
        list_display = super().get_list_display(request)
        return list_display + ("published_state",)

    def render_change_form(self, request, context, *args, **kwargs):
        """
        Render the change form for the admin.

        Args:
            request (HttpRequest): The request object.
            context (dict): The context for the form.

        Returns:
            HttpResponse: The rendered change form.
        """
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
        """
        Render the changelist view for the admin.

        Args:
            request (HttpRequest): The request object.
            extra_context (dict, optional): Extra context for the view.

        Returns:
            HttpResponse: The rendered changelist view.
        """
        if request.POST and "action" in request.POST:
            context = {
                "has_change_permission": self.has_change_permission(request),
            }
            context.update(extra_context or {})
            return super(VersionAdmin, self).changelist_view(request, context)
        else:
            return super().changelist_view(request, extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        """
        Render the change view for the admin.

        Args:
            request (HttpRequest): The request object.
            object_id (str): The ID of the object being changed.
            form_url (str, optional): The form URL.
            extra_context (dict, optional): Extra context for the view.

        Returns:
            HttpResponse: The rendered change view.
        """
        obj: LocalizedPublicationModel = self.get_object(request, unquote(object_id))

        request_post_keys = set(request.POST.keys())

        if not HEADLESS_CMS_ACTIONS.isdisjoint(request_post_keys):
            res = self.changeform_view(request, object_id, form_url, extra_context)

            if "_unpublish" in request_post_keys:
                obj.unpublish(request.user)
            elif "_publish" in request_post_keys:
                obj.publish(request.user)
            elif "_recursively_publish" in request_post_keys:
                obj.recursively_publish(request.user)
            elif not TRANSLATE_ACTIONS.isdisjoint(request_post_keys):
                force = not FORCE_TRANSLATE.isdisjoint(request_post_keys)
                recursively = not RECURSIVELY_TRANSLATE.isdisjoint(request_post_keys)
                if recursively:
                    obj.recursively_translate(request.user, force)
                else:
                    obj.translate(request.user, force)
            return res
        else:
            return super().change_view(request, object_id, form_url, extra_context)

    def response_change(self, request, obj):
        """
        Handle the response after saving the object in the admin.

        Args:
            request (HttpRequest): The request object.
            obj (models.Model): The object being saved.

        Returns:
            HttpResponse: The response.
        """
        opts = self.opts
        preserved_filters = self.get_preserved_filters(request)

        msg_dict = {
            "name": opts.verbose_name,
            "obj": format_html('<a href="{}">{}</a>', urlquote(request.path), obj),
        }

        custom_actions = {
            "_publish",
            "_unpublish",
            "_recursively_publish",
        } | TRANSLATE_ACTIONS

        request_post_keys = set(request.POST.keys())

        if custom_actions.isdisjoint(request_post_keys):
            # Default behavior
            return super().response_change(request, obj)

        if "_publish" in request_post_keys:
            msg = format_html(
                _("The {name} “{obj}” was published successfully."),
                **msg_dict,
            )
        elif "_recursively_publish" in request_post_keys:
            msg = format_html(
                _("The {name} “{obj}” was recursively published."),
                **msg_dict,
            )
        elif "_unpublish" in request_post_keys:
            msg = format_html(
                _("The {name} “{obj}” was unpublished."),
                **msg_dict,
            )
        elif not TRANSLATE_ACTIONS.isdisjoint(request_post_keys):
            force = not FORCE_TRANSLATE.isdisjoint(request_post_keys)
            recursively = not RECURSIVELY_TRANSLATE.isdisjoint(request_post_keys)

            recursively_text = " recursively" if recursively else ""
            force_text = " (forced)" if force else ""

            msg = format_html(
                _(
                    f"The {{name}} “{{obj}}” was{recursively_text} translated{force_text}."
                ),
                **msg_dict,
            )
        else:
            msg = _("Invalid action")
        self.message_user(request, msg, messages.SUCCESS)
        redirect_url = request.path
        redirect_url = add_preserved_filters(
            {"preserved_filters": preserved_filters, "opts": opts}, redirect_url
        )
        return HttpResponseRedirect(redirect_url)

    def revision_view(self, request, object_id, version_id, extra_context=None):
        """
        Displays the contents of the given revision.

        Args:
            request (HttpRequest): The request object.
            object_id (str): The ID of the object being changed.
            version_id (str): The ID of the version to display.
            extra_context (dict, optional): Extra context for the view.

        Returns:
            HttpResponse: The rendered revision view.
        """
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
        """
        Helper method for rendering the revision form view.

        Args:
            request (HttpRequest): The request object.
            version (Version): The version to display.
            template_name (str): The template name.
            extra_context (dict, optional): Extra context for the view.

        Returns:
            HttpResponse: The rendered revision form view.
        """
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

    def get_resource_classes(self, *args, **kwargs):
        """
        Get the resource classes for import/export.

        Returns:
            list: The resource classes.
        """
        if not self.resource_classes:
            return [override_modelresource_factory(self.model)]
        return super().get_resource_classes(*args, **kwargs)


@lru_cache(maxsize=0)
def create_m2m_inline_admin(model, sortable=False, fk_name=None):
    """
    Create an inline admin class for a many-to-many relationship.

    Args:
        model (models.Model): The model for the inline admin.
        sortable (bool, optional): Whether the inline is sortable.
        fk_name (str, optional): The foreign key name.

    Returns:
        type: The inline admin class.
    """
    body = {"extra": 0, "model": model}
    if fk_name is not None:
        body["fk_name"] = fk_name
    return type(
        model.__name__ + "Inline",
        (
            PublishStatusInlineMixin,
            SortableStackedInline if sortable else StackedInline,
        ),
        body,
    )


@lru_cache(maxsize=0)
def create_generic_inline_admin(model, sortable=False):
    """
    Create an inline admin class for a generic relationship.

    Args:
        model (models.Model): The model for the inline admin.
        sortable (bool, optional): Whether the inline is sortable.

    Returns:
        type: The inline admin class.
    """
    return type(
        model.__name__ + "Inline",
        (BaseSortableGenericAdmin if sortable else BaseGenericAdmin,),
        {"model": model},
    )


def auto_admins(
    model_list: list[type[models.Model]],
):
    """
    Automatically register admin classes for a list of models.

    Args:
        model_list (list): The list of models to register.
    """
    for model in model_list:
        admin_attrs = {"history_latest_first": True}
        inlines = []
        exclude = []
        readonly_fields = []
        model_fields = model._meta.get_fields()
        has_sortable_base = False
        for field in model_fields:
            if isinstance(field, LocalizedUniqueNormalizedSlugField):
                readonly_fields.append(field.name)

            if isinstance(field, ManyToManyField) and issubclass(
                field.related_model, LocalizedPublicationModel
            ):
                through = getattr(model, field.name).through
                exclude.append(field.name)

                can_sort = False
                if issubclass(through, M2MSortedOrderThrough):
                    can_sort = True
                    has_sortable_base = True

                fk_name = getattr(through, "fk_name", None)

                inlines.append(create_m2m_inline_admin(through, can_sort, fk_name))
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
        admin_attrs["readonly_fields"] = readonly_fields

        base_admin = []
        if has_sortable_base:
            base_admin = [SortableAdminBase]

        base_admin.append(EnhancedLocalizedVersionAdmin)

        if issubclass(model, LocalizedSingletonModel):
            base_admin.append(SingletonModelAdmin)

        admin_model = type(model.__name__ + "Admin", tuple(base_admin), admin_attrs)
        admin.site.register(model, admin_model)
