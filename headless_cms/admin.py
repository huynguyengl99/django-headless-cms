from urllib.parse import quote as urlquote

import reversion
from django.contrib import admin, messages
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.admin.utils import unquote
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.html import format_html
from django.utils.translation import gettext as _
from localized_fields.admin import LocalizedFieldsAdminMixin
from martor.widgets import AdminMartorWidget
from rest_framework import status
from reversion.admin import VersionAdmin
from reversion.models import Version

from headless_cms.settings import headless_cms_settings


class PublishStatusInlineMixin:
    show_change_link = True

    readonly_fields = ("publish_status",)

    def publish_status(self, obj):
        published_state = "unpublished"
        if obj.published_version:
            last_ver = Version.objects.get_for_object(obj).first()
            if last_ver.id == obj.published_version.id:
                published_state = "published (latest)"
            else:
                published_state = "published (outdated)"
        return published_state


@admin.action(description="Publish selected")
def publish(modeladmin, request, queryset):
    for obj in queryset.all():
        with reversion.create_revision():
            reversion.set_comment("Publish")
            reversion.set_user(request.user)

            obj.save()

        with reversion.create_revision(manage_manually=True):
            last_ver = Version.objects.get_for_object(obj).first()

            obj.published_version = last_ver
            obj.save()


class EnhancedLocalizedVersionAdmin(LocalizedFieldsAdminMixin, VersionAdmin):
    actions = [publish]
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
            reversion.set_comment(f"Object translated{' (forced)' if force else ''}.")

            translator = headless_cms_settings.AUTO_TRANSLATE_CLASS(obj)
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
