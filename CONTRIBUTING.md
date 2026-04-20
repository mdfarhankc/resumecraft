# Contributing to ResumeCraft

Thanks for your interest in contributing! Here's how to get set up.

## Setup

```bash
git clone https://github.com/mdfarhankc/resumecraft.git
cd resumecraft
uv sync --all-extras
```

## Running tests

```bash
uv run pytest
```

## Linting and type checks

```bash
uv run ruff check src/ tests/
uv run mypy src/
```

Both should pass before opening a PR. Auto-fix what you can with:

```bash
uv run ruff check --fix src/ tests/
```

## Submitting changes

1. Fork the repo and create a feature branch.
2. Make your changes, add tests, and make sure `pytest`, `ruff`, and `mypy` all pass.
3. Open a PR with a short description of what changed and why.

## Adding a new section type

If you're adding a new resume section (like a new kind of experience):

1. Add the Pydantic model to `src/resumecraft/models.py`.
2. Add it to the `Resume` class and to `SectionName` + `DEFAULT_SECTION_ORDER`.
3. Add a `_build_<name>` method in `src/resumecraft/builder.py` and register it in the `section_builders` map in `build()`.
4. Add a default heading in `DEFAULT_HEADINGS`.
5. Update `ResumeCraft.sample()` and the CLI template in `cli.py`.
6. Add tests in `tests/test_builder.py` and `tests/test_models.py`.

## Reporting bugs

Open an issue with a minimal JSON file that reproduces the problem and the output/error you got.
