# Repo Maintenance Guidelines

This repository is a Python project that simulates cab allocation. Follow these instructions when updating files in this repo so automated agents know how to operate.

## Environment Setup
- Use **Python 3.11**.
- Install dependencies with `pip install -e .[dev]` or by running `make dev`.

## Running Tests
- Execute `pytest --cov=cab_allocator` from the repository root to run all tests.
- Always run the tests after modifying code or documentation.

## Coding Conventions
- Follow standard PEP8 style. There are no additional linters configured.
- Keep imports ordered logically and avoid unused imports.

