.PHONY: install test lint fix typecheck check build clean schema

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

schema:
	uv run python -c "import json; from resumecraft import ResumeCraft; s = ResumeCraft.json_schema(); s['\$$schema'] = 'http://json-schema.org/draft-07/schema#'; s['title'] = 'ResumeCraft Resume'; open('resumecraft-schema.json', 'w').write(json.dumps(s, indent=2))"

clean:
	rm -rf dist/ build/ *.egg-info .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov/
