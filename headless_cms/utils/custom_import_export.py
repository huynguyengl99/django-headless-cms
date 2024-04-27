from import_export.resources import ModelDeclarativeMetaclass, ModelResource


def override_modelresource_factory(model, resource_class=ModelResource):
    """
    Factory for creating ``ModelResource`` class for given Django model.
    """
    attrs = {
        "model": model,
        "exclude": ["published_version"],
        "use_natural_foreign_keys": True,
    }
    Meta = type("Meta", (object,), attrs)  # noqa

    class_name = model.__name__ + "Resource"

    class_attrs = {
        "Meta": Meta,
    }

    metaclass = ModelDeclarativeMetaclass
    return metaclass(class_name, (resource_class,), class_attrs)
