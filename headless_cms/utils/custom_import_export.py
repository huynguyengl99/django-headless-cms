import reversion
from django.db.models import ManyToManyField
from django.utils.translation import gettext_lazy as _
from import_export import widgets
from import_export.resources import ModelDeclarativeMetaclass, ModelResource
from import_export.widgets import Widget
from localized_fields.fields import LocalizedField, LocalizedFileField


class LocalizedWidget(Widget):
    def render(self, value, obj=None):
        return value


class LocalizedFileWidget(LocalizedWidget):
    def render(self, value, obj=None):
        return {k: "" for k, _v in value.__dict__.items()}


class LocalizedModelResource(ModelResource):
    @classmethod
    def widget_from_django_field(cls, f, default=widgets.Widget):
        if isinstance(f, LocalizedFileField):
            return LocalizedFileWidget
        elif isinstance(f, LocalizedField):
            return LocalizedWidget
        return super().widget_from_django_field(f, default)

    def save_instance(self, *args, **kwargs):
        with reversion.create_revision():
            reversion.set_comment(_("Import data"))
            super().save_instance(*args, **kwargs)


def override_modelresource_factory(
    model, resource_class=LocalizedModelResource, exclude_m2m=False
):
    """
    Factory for creating ``ModelResource`` class for given Django model.
    """
    exclude = ["published_version"]
    if exclude_m2m:
        model_fields = model._meta.get_fields()
        for field in model_fields:
            if isinstance(field, ManyToManyField):
                exclude.append(field.name)

    attrs = {
        "model": model,
        "exclude": exclude,
        "use_natural_foreign_keys": True,
        "skip_unchanged": True,
    }
    Meta = type("Meta", (object,), attrs)  # noqa

    class_name = model.__name__ + "Resource"

    class_attrs = {
        "Meta": Meta,
    }

    metaclass = ModelDeclarativeMetaclass
    return metaclass(class_name, (resource_class,), class_attrs)
