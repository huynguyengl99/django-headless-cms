from localized_fields.fields import LocalizedField
from localized_fields.value import LocalizedStringValue

from ..forms import LocalizedMartorForm
from ..widgets import AdminLocalizedMartorWidget


class LocalizedMartorField(LocalizedField):
    """
    A custom field that provides a localized Markdown editor with multi-language support.
    It extends the LocalizedField and uses LocalizedStringValue for storing values.

    The field utilizes the LocalizedMartorForm and AdminLocalizedMartorWidget to render
    the Markdown editor in the admin interface.
    """

    attr_class = LocalizedStringValue

    def formfield(self, **kwargs):
        kwargs.pop("widget", None)

        defaults = {
            "form_class": LocalizedMartorForm,
            "widget": AdminLocalizedMartorWidget,
        }

        defaults.update(kwargs)
        return super().formfield(**defaults)
