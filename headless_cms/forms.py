from django.forms import SlugField
from localized_fields.forms import LocalizedCharFieldForm, LocalizedFieldForm
from localized_fields.value import LocalizedStringValue
from martor.fields import MartorFormField

from .widgets import LocalizedMartorWidget


class LocalizedMartorForm(LocalizedFieldForm):
    """Form for a localized integer field, allows editing the field in multiple
    languages."""

    widget = LocalizedMartorWidget
    field_class = MartorFormField
    value_class = LocalizedStringValue


class LocalizedSlugForm(LocalizedCharFieldForm):
    """Form for a localized integer field, allows editing the field in multiple
    languages."""

    field_class = SlugField
    value_class = LocalizedStringValue
