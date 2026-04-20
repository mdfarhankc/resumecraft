.PHONY: install test lint fix typecheck check build clean

install:
	uv sync --all-extras

test:
	uv run pytest

lint:
	uv run ruff check src/ tests/

fix:
	uv run ruff check --fix src/ tests/

typecheck:
	uv run mypy src/

check: lint typecheck test

build:
	uv build

clean:
	rm -rf dist/ build/ *.egg-info .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov/
