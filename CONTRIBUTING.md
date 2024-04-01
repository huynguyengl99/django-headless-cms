# Contributing to django-headless-cms

Contributions are welcome! Here are some pointers to help you install the library for development and validate your changes before submitting a pull request.

## Install the library for development

First create your own `venv` and activate it:

```bash
pythin -m venv .venv
source .venv/bin/activate
```

Then we recommend installing the module in editable mode with the `dev` extra requirements:
```bash
pip install -e ".[dev]" -r requirements.txt
```

To check it worked, use:
```bash
$ which pip
```
Result:
```console
some/directory/django-headless-cms/.venv/bin/pip
```

## Validate the changes before creating a pull request
0. Prepare for test:
- Docker running
- Run `docker-compose up` to create testing postgresql database.

1. Make sure the existing tests are still passing (and consider adding new tests as well!):

```bash
pytest --cov-report term-missing --cov=headless_cms tests
```

2. Reformat and validate the code with the following tools:

```bash
bash scripts/lint.sh [--fix]
```

These steps are also run automatically in the CI when you open the pull request.
