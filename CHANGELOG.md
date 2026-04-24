# Changelog

## v0.5.1

### Changed
- `typer` is a core dependency again so `uvx resumecraft` and `pipx install resumecraft` work without the `[cli]` extra. The `[cli]` extra is kept as a no-op for backward compat.

### Fixed
- CLI now shows a clear error (instead of a Python traceback) when passed a non-JSON file or a binary file.

## v0.5.0

### Added
- `certifications` section with issuer, date, and optional verification link
- `awards` section with title, issuer, date, and optional description
- Multi-link support for projects and certifications via `links` field
- Custom section headings via `headings` field
- `style.ats` option to strip formatting that confuses ATS parsers
- JSON schema shipped in the wheel for `$schema` editor autocomplete
- Ruff and mypy with strict typing
- pytest-cov and codecov upload to CI
- Makefile for common dev tasks (`make test`, `make lint`, `make fix`, `make check`)

### Changed
- Watch mode now logs build failures to stderr instead of silently swallowing them

### Fixed
- Validate required contact fields (location, email, phone must be non-empty)

## v0.4.0

### Changed
- Watch mode defaults to PDF output (PDF viewers don't lock files)
- Watch mode derives output filename from input when `-o` is omitted

### Added
- `--open` flag to watch command

### Fixed
- Graceful error handling when output file is locked

## v0.3.0

### Added
- `ResumeCraft` class with `from_json()`, `to_docx()`, `to_pdf()`, `to_bytes()`
- Unified `projects` section alongside split professional/personal
- Style options: 7 fonts, 6 color themes, 3 spacing presets
- `json_schema()`, `to_dict()`, `sample()`, `__repr__()` on ResumeCraft
- `examples/` folder
- `[all]` extra for installing everything
- Accept JSON strings in ResumeCraft constructor

### Changed
- CLI is now optional (`typer` moved to `[cli]` extra)

## v0.2.0

### Added
- Custom section ordering via `section_order`
- Watch mode for auto-rebuild on file changes
- `--open` flag to open output after building
- Timestamped default output filenames
- Optional PDF output via `docx2pdf`

## v0.1.0

Initial release.

### Added
- JSON-driven resume generation to `.docx`
- Auto bold keywords, right-aligned dates, clickable hyperlinks
- Pydantic validation, smart page breaks
- CLI commands: `build`, `validate`, `init`
