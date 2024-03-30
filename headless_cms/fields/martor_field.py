from localized_fields.fields import LocalizedField
from localized_fields.value import LocalizedStringValue

from ..forms import LocalizedMartorForm
from ..widgets import AdminLocalizedMartorWidget


class LocalizedMartorField(LocalizedField):
    attr_class = LocalizedStringValue

    def formfield(self, **kwargs):
        kwargs.pop("widget", None)

        defaults = {
            "form_class": LocalizedMartorForm,
            "widget": AdminLocalizedMartorWidget,
        }

        defaults.update(kwargs)
        return super().formfield(**defaults)
