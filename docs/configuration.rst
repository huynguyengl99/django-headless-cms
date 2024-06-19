=====================
Configuration
=====================

Headless CMS Settings
=====================

The `django-headless-cms` package can be customized using various settings. These settings should be added to your Django project's settings file under the `HEADLESS_CMS_SETTINGS` dictionary.

Here is the structure of the configuration with detailed comments explaining each setting:

.. code-block:: python

    # settings.py

    HEADLESS_CMS_SETTINGS = {
        # The class used for automatic translation of content.
        # Alternative, using ChatGPT: "headless_cms.auto_translate.openai_translate.OpenAITranslate"
        # You can create a translation class yourself by inheriting from BaseTranslate.
        "AUTO_TRANSLATE_CLASS": "headless_cms.auto_translate.BaseTranslate",

        # Preprocessing hooks for DRF Spectacular.
        "CMS_DRF_SPECTACULAR_PREPROCESSING_HOOKS": [
            "headless_cms.schema.preprocessing_hooks.preprocessing_filter_spec"
        ],

        # List of terms to ignore during auto-translation.
        "AUTO_TRANSLATE_IGNORES": [],

        # List of fields to exclude from serialization.
        "GLOBAL_EXCLUDED_SERIALIZED_FIELDS": [],

        # The OpenAI model to use for chat-based translation.
        # The default model is gpt-4-turbo because we find it slightly better than gpt-4.
        # But you can choose any model you want here.
        "OPENAI_CHAT_MODEL": "gpt-4-turbo",

        # The OpenAI client to use for translation.
        "OPENAI_CLIENT": "openai.OpenAI",

        # The default permission class for the CMS.
        "DEFAULT_CMS_PERMISSION_CLASS": "rest_framework.permissions.AllowAny",

        # The host URL of the CMS.
        # Normally, this is applied for localhost.
        # For production, if you use django-storage, you don't need to configure this.
        "CMS_HOST": "http://localhost:8000",
    }

Example Configuration
=====================

Below is an example configuration that demonstrates how to customize the settings for `django-headless-cms`:

.. code-block:: python

    # settings.py

    HEADLESS_CMS_SETTINGS = {
        "AUTO_TRANSLATE_CLASS": (
            "headless_cms.auto_translate.openai_translate.OpenAITranslate"
        ),
        "AUTO_TRANSLATE_IGNORES": [
            "Astro",
            "Astrowind",
            "Tailwind CSS",
        ],
        "OPENAI_CHAT_MODEL": "gpt-4",
        "DEFAULT_CMS_PERMISSION_CLASS": "rest_framework_api_key.permissions.HasAPIKey",
    }
