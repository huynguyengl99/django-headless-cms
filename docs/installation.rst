==============================
Installation
==============================

django-headless-cms is available on the Python Package Index (PyPI), so it
can be installed with standard Python tools like ``pip`` or ``poetry``.

Installation Methods
--------------------

.. contents::
   :local:
   :depth: 1

Using pip
~~~~~~~~~

You can install django-headless-cms using pip:

.. code-block:: shell

    pip install django-headless-cms

Optional dependencies for OpenAI support can be installed with:

.. code-block:: shell

    pip install django-headless-cms[openai]

Using Poetry
~~~~~~~~~~~~

If you're using Poetry for dependency management, you can add django-headless-cms to your project with:

.. code-block:: shell

    poetry add django-headless-cms

To include optional dependencies, you can specify the extra:

.. code-block:: shell

    poetry add django-headless-cms -E openai

Development Version
~~~~~~~~~~~~~~~~~~~

Alternatively, you can install the git repository directly to obtain the development version:

.. code-block:: shell

    pip install -e git+https://github.com/huynguyengl99/django-headless-cms.git#egg=django-headless-cms
