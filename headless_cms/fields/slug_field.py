from localized_fields.fields import LocalizedCharField
from localized_fields.value import LocalizedStringValue

from ..forms import LocalizedSlugForm


class LocalizedSlugField(LocalizedCharField):
    attr_class = LocalizedStringValue

    def formfield(self, **kwargs):
        """Gets the form field associated with this field."""
        defaults = {"form_class": LocalizedSlugForm}

        defaults.update(kwargs)
        return super().formfield(**defaults)
