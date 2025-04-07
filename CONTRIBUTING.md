# Contributing to django-headless-cms

Contributions are welcome! Here are some pointers to help you install the library for development and validate your changes before submitting a pull request.

## Install the library for development


First install [uv](https://docs.astral.sh/uv/getting-started/installation/), create your own `.venv`
and activate it:

```bash
uv venv # or pythin -m venv .venv
source .venv/bin/activate
```

Then use uv install all dev package:
```bash
uv sync
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
