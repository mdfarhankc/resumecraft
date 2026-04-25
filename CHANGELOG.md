# Changelog

## v0.6.0

### Added
- `ResumeCraft.from_jsonfile`, `from_json` (string), `from_bytes`, `from_dict` factory methods. `from_bytes` handles UTF-8 BOM and rejects binary input cleanly.
- YAML input via `ResumeCraft.from_yamlfile` and `from_yaml`, plus a new `[yaml]` extra. CLI's `build` and `watch` auto-detect `.yaml` / `.yml`.
- `to_docx_bytes()` and `to_pdf_bytes()` for in-memory exports.
- `--pdf` flag on `build` as a shortcut for `-o <input-name>.pdf`.
- Reject duplicate entries in `section_order` at validation time.
- Strict field validation: typos in JSON keys (e.g. `experiance` instead of `experience`) now raise instead of being silently ignored.
- Python 3.14 in the CI test matrix.

### Changed
- Internal refactor: rendering is now split into `sections.py` (Section classes + registry) and `render.py` (RenderContext + paragraph helpers). `DocxBuilder` shrunk from ~330 lines to ~70. Output is byte-identical.
- `ResumeCraft` is the only class exported at the top level. `Resume` and `DocxBuilder` are still importable from `resumecraft.models` and `resumecraft.builder`.
- `typer` is a core dependency again so `uvx resumecraft` and `pipx install resumecraft` work without the `[cli]` extra. The `[cli]` extra is kept as a no-op for backward compat.
- Default output filename now uses the input file's stem, e.g. `my-resume_2026-04-24_11-33pm.docx` instead of `resume_...docx`.
- CLI catches output-path errors (locked files, directories, disk issues) with a clear message instead of a traceback.
- Examples folder collapsed to `library.py` and `web.py`.

### Deprecated
- `ResumeCraft(dict)` and `ResumeCraft(json_string)` — use `ResumeCraft.from_dict()` / `from_json()`.
- `ResumeCraft.from_json(file_path)` — use `ResumeCraft.from_jsonfile(path)`.
- `ResumeCraft.to_bytes()` — use `to_docx_bytes()`.

### Fixed
- CLI shows a clear error (instead of a Python traceback) when passed a non-JSON or binary file.
- PDF temp file is cleaned up even if the PDF conversion fails.

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
