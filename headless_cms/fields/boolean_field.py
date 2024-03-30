from django.conf import settings
from localized_fields.fields import LocalizedBooleanField as BaseLocalizedBooleanField
from localized_fields.value import LocalizedBooleanValue, LocalizedValue


class LocalizedBooleanField(BaseLocalizedBooleanField):
    @staticmethod
    def _convert_localized_value(
        value: LocalizedValue,
    ) -> LocalizedBooleanValue:
        """Converts from :see:LocalizedValue to :see:LocalizedBooleanValue."""

        integer_values = {}
        for lang_code, _ in settings.LANGUAGES:
            local_value = value.get(lang_code, None)

            if isinstance(local_value, bool):
                integer_values[lang_code] = local_value
            elif isinstance(local_value, str):
                if local_value.lower() == "false":
                    local_value = False
                elif local_value.lower() == "true":
                    local_value = True
                else:
                    raise ValueError(
                        f"Could not convert value {local_value} to boolean."
                    )

                integer_values[lang_code] = local_value
            elif local_value is not None:
                raise TypeError(
                    f"Expected value of type str instead of {type(local_value)}."
                )

        return LocalizedBooleanValue(integer_values)
