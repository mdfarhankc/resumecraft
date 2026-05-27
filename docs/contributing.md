# Contributing

## Setup

```bash
git clone https://github.com/mdfarhankc/resumecraft.git
cd resumecraft
uv sync --all-extras
```

## Running Tests

```bash
uv run pytest                             # run all tests
uv run pytest --tb=short -q               # compact output
uv run pytest tests/test_builder.py -k photo  # run specific tests
```

## Linting and Type Checking

```bash
uv run ruff check src/ tests/            # lint
uv run ruff check --fix src/ tests/       # auto-fix
uv run mypy src/                          # type check (strict mode)
```

## Building the Docs

```bash
uv sync --extra docs
uv run mkdocs serve                       # live preview at http://127.0.0.1:8000
uv run mkdocs build                       # build static site to site/
```

## Building the Package

```bash
uv build
```

Creates `dist/resumecraft-x.x.x.tar.gz` and `dist/resumecraft-x.x.x-py3-none-any.whl`.

## Publishing

Tag a GitHub release (e.g., `v0.7.0`) and the CI workflow publishes to PyPI automatically via trusted publishing.

## Project Structure

```
resumecraft/
├── pyproject.toml                  # package metadata and dependencies
├── mkdocs.yml                      # docs site config
├── schema.json                     # JSON schema for editor autocomplete
├── docs/                           # documentation source (MkDocs)
├── examples/
│   ├── library.py                  # library usage example
│   ├── web.py                      # web framework example
│   ├── sample_resume.json          # complete sample resume
│   └── output/sample_resume.pdf    # generated PDF
├── src/resumecraft/
│   ├── __init__.py                 # public exports: ResumeCraft, __version__
│   ├── craft.py                    # ResumeCraft class (factory methods, exports)
│   ├── cli.py                      # CLI commands (Typer)
│   ├── builder.py                  # DocxBuilder (orchestrates rendering)
│   ├── sections.py                 # Section classes + SECTION_REGISTRY
│   ├── render.py                   # RenderContext + paragraph helpers
│   ├── models.py                   # Pydantic data models
│   ├── styles.py                   # font/color/spacing maps and constants
│   ├── samples.py                  # sample resume data
│   └── utils.py                    # low-level docx helpers
└── tests/
    ├── conftest.py                 # shared fixtures
    ├── fixtures/sample.json        # test data
    ├── test_models.py
    ├── test_builder.py
    ├── test_craft.py
    ├── test_cli.py
    └── test_utils.py
```

## Architecture

```
JSON/YAML → Resume (Pydantic model) → DocxBuilder → Section classes → python-docx Document
                                          ↓
                                    RenderContext (style, fonts, colors)
```

1. **Models** (`models.py`) - Pydantic v2 models with strict validation
2. **Styles** (`styles.py`) - Font, color, and spacing resolution
3. **Sections** (`sections.py`) - Each section type has a class that knows how to render itself
4. **Render** (`render.py`) - Shared rendering functions (runs, headings, bullets, two-column lines)
5. **Builder** (`builder.py`) - Orchestrates document creation, sets up margins and fonts
6. **Craft** (`craft.py`) - Public API with factory methods and export methods
7. **CLI** (`cli.py`) - Typer-based CLI wrapping the library
