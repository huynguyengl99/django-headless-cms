from django.db.models import CharField
from localized_fields.fields import LocalizedCharField


class AutoLanguageUrlField(CharField):
    """This field will automatically add language prefix path for relative url (/about => /en/about)
    but will keep the full url as it is."""

    pass


class LocalizedUrlField(LocalizedCharField):
    """This field is used to prevent automatic translation for this field (the link should remain stable)."""

    pass
