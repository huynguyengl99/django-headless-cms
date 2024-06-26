#!/usr/bin/env bash

if [ "$1" == "--fix" ]; then
  ruff check . --fix && black ./headless_cms && toml-sort pyproject.toml
else
  ruff check . && black ./headless_cms --check && toml-sort pyproject.toml --check
fi
