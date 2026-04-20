# Changelog

## v0.5.0

- Add `certifications` section with issuer, date, and optional verification link
- Add `awards` section with title, issuer, date, and optional description
- Add multi-link support for projects and certifications via `links` field (legacy `link` still works)
- Add custom section headings via `headings` field
- Add `style.ats` option to strip formatting that confuses ATS parsers
- Ship JSON schema in the wheel for `$schema` editor autocomplete
- Validate required contact fields (location, email, phone must be non-empty)
- Watch mode now logs build failures to stderr instead of silently swallowing them
- Add ruff and mypy with strict typing
- Add pytest-cov and codecov upload to CI
- Add Makefile for common dev tasks (`make test`, `make lint`, `make fix`, `make check`)

## v0.4.0

- Watch mode defaults to PDF output (PDF viewers don't lock files)
- Watch mode derives output filename from input when `-o` is omitted
- Add `--open` flag to watch command
- Graceful error handling when output file is locked

## v0.3.0

- Add `ResumeCraft` class with `from_json()`, `to_docx()`, `to_pdf()`, `to_bytes()`
- CLI is now optional (`typer` moved to `[cli]` extra)
- Add `[all]` extra for installing everything
- Add unified `projects` section alongside split professional/personal
- Style options: 7 fonts, 6 color themes, 3 spacing presets
- Add `json_schema()`, `to_dict()`, `sample()`, `__repr__()` on ResumeCraft
- Accept JSON strings in ResumeCraft constructor
- Add `examples/` folder

## v0.2.0

- Custom section ordering via `section_order`
- Watch mode for auto-rebuild on file changes
- `--open` flag to open output after building
- Timestamped default output filenames
- Optional PDF output via `docx2pdf`

## v0.1.0

- Initial release
- JSON-driven resume generation to `.docx`
- Auto bold keywords, right-aligned dates, clickable hyperlinks
- Pydantic validation, smart page breaks
- CLI commands: `build`, `validate`, `init`
