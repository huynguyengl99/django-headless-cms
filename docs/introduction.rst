Introduction
============

Why Choose Django-headless-cms?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Why choose Django-headless-cms over alternatives like `Wagtail <https://wagtail.org/>`_,
`Django-CMS <https://www.django-cms.org/>`_, `Strapi <https://strapi.io/>`_, or
`Contentful <https://www.contentful.com/>`_?

- **Headless CMS with minimal configuration**: Unlike Wagtail and Django-CMS, which are primarily headed CMS solutions.
- **Responsive UI**: Preferred over Strapi for its user interface.
- **Python & Django-based**: Built on a robust framework with numerous extensions.
- **Open Source**: Unlike Contentful and other paid services, it allows you to self-host your CMS.
- **Integration**: Easily integrates with many existing Python and Django libraries.
- **Centralized multi-language support**: Reduces redundancy and allows different content across multiple languages.

Features
~~~~~~~~

- **Schema Migrations**: Manage content schema as database migrations, making it easier to sync from development to
  production environments.
- **Versioning Content**: Revert to any previously saved version.
- **Publish/Draft Content**: Manage published and draft content.
- **Markdown Editor Support**: Enhanced content editing experience, useful for Posts/Articles.
- **Multi-language Support**: Even for Markdown fields.
- **Auto Translate/Force Re-translate**: Use ChatGPT or build your own translation interface.
- **Recursive Actions**: Apply actions like Publish, Translate, and Force Re-translate to referenced objects.
- **Optimized Queries**: Auto prefetch and select related queries for optimization.
- **Filter Published Objects**: Easily filter to show only published content.
- **Auto Admin**: Simplify admin page setup with features like:
  -. Sortable inline Many-to-Many (M2M) relationships.
  -. Sortable generic inlines.
  -. Display publish status of child objects.
- **Auto Serializer**: Simplify serializer creation, including nested relations. Override specific serializers as needed.
- **Rapid API Development**: Build APIs (Views/Viewsets) quickly and easily with auto serializers and optimized queries.
- **Easy Data Import/Export**: Use the admin interface or management commands.
- **Auto-generated API Documentation & Playground**: Automatically generate API documentation and an interactive playground.
- **Hash**: Provide hash utilities to check whether an object (and its descendant children) has changed or not (thanks
  to versioning). This can be helpful in building caching mechanisms to reduce API calls and improve performance.

Dependencies
~~~~~~~~~~~~

Special thanks to these outstanding packages that have been used as supporting components within Django-headless-cms:

- `Django-localized-fields <https://github.com/SectorLabs/django-localized-fields>`_: Supports multi-language fields.
- `django-markdown-editor (Martor) <https://github.com/agusmakmun/django-markdown-editor>`_: Provides a markdown editor.
- `Django-reversion <https://github.com/etianen/django-reversion>`_: Offers versioning and publish/draft content support.
- `Django-admin-interface <https://github.com/fabiocaccamo/django-admin-interface>`_: Enhances the Django admin
  interface and supports language switching.
- `Django-solo <https://github.com/lazybird/django-solo>`_: Supports singleton admin models.
- `Django-import-export <https://github.com/django-import-export/django-import-export>`_: Facilitates data import and export.
- `Django-filter <https://github.com/carltongibson/django-filter>`_: Assists in building API query filters.
- `Unidecode <https://pypi.org/project/Unidecode/>`_: Helps create readable slug URLs.
- `OpenAI <https://github.com/openai/openai-python>`_: Enables auto-translation with ChatGPT.
- `Django <https://www.djangoproject.com/>`_ & `Django REST framework <https://www.django-rest-framework.org/>`_:
  The foundational frameworks.

[Extra] My Story
~~~~~~~~~~~~~~~~

After experimenting with various CMS frameworks, I couldn't find a suitable one for my needs:

- **Strapi**: Node.js-based and synchronizing schema between development and production can be challenging.
  Additionally, it lacks a responsive UI, making minor updates on mobile devices difficult.
- **Wagtail and Django-CMS**: These are headed CMS solutions, great if you need a WYSIWYG CMS. However, they felt
  overly complex for my use case and have a steep learning curve.
- **Contentful & other paid services**: While these services are excellent, their costs can be prohibitive. Why pay
  for additional slots when you can add them for free in Django?

After further research into Django-based (and Node.js-based) frameworks, I found none that met my expectations. Given
Django's popularity and extensive ecosystem of extensions, I decided to build Django-headless-cms. I also noticed that
some Reddit users faced similar issues, which motivated me to create this package.

If you appreciate this package, please give it a star. If you'd like to see more features, consider contributing. If
you encounter any issues, don't hesitate to open a GitHub issue (and help fix it if you're willing to contribute).
