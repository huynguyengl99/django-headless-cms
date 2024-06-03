Commands
========

This section provides documentation on the various management commands available in the headless CMS.

Clean Outdated Drafts
---------------------

Deletes outdated drafts.

Usage:

.. code-block:: shell

    python manage.py clean_outdated_drafts --days <number_of_days>

Options:
    --days: Delete only revisions older than the specified number of days.

.. autofunction:: headless_cms.core.management.commands.clean_outdated_drafts.Command

Export CMS Data
---------------

Exports data recursively of a Django app into JSON files.

Usage:

.. code-block:: shell

    python manage.py export_cms_data --output <output_directory> [--compress] [--cf <compress_format>]

Options:
    --output: Export data to this directory.
    --compress: Compress data.
    --cf, --compress-format: Compression format (default is zip).

.. autofunction:: headless_cms.core.management.commands.export_cms_data.Command

Import CMS Data
---------------

Imports data recursively of a Django app from JSON files.

Usage:

.. code-block:: shell

    python manage.py import_cms_data --input <input_directory_or_file> [--cf <compress_format>]

Options:
    --input: Directory or compression file to import data from.
    --cf, --compress-format: Compression format (default is zip).

.. autofunction:: headless_cms.core.management.commands.import_cms_data.Command

Populate Astrowind Data
-----------------------

Populates Astrowind data.

Usage:

.. code-block:: shell

    python manage.py populate_aw_data

.. autofunction:: headless_cms.contrib.astrowind.astrowind_pages.management.commands.populate_aw_data.Command
