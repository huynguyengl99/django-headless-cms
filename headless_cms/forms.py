from typing import Union

from localized_fields.forms import LocalizedFieldForm
from localized_fields.value import LocalizedStringValue
from martor.fields import MartorFormField

from .widgets import LocalizedMartorWidget


class _LocalizedMartorField(LocalizedFieldForm):
    def __init__(self, *args, required: Union[bool, list[str]] = False, **kwargs):
        kwargs.pop("label", None)
        super().__init__(*args, required=required, **kwargs)


class LocalizedMartorForm(LocalizedFieldForm):
    """Form for a localized integer field, allows editing the field in multiple
    languages."""

    widget = LocalizedMartorWidget
    field_class = MartorFormField
    value_class = LocalizedStringValue
