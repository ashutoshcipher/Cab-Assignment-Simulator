.PHONY: dev test

dev:
pip install -e .[dev]

test:
pytest --cov=cab_allocator

