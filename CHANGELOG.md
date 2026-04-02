# Changelog

## v0.3.0

- Add `ResumeCraft` class — simple high-level API with `from_json()`, `to_docx()`, and `to_bytes()`
- Make CLI optional — `typer` moved to `[cli]` extra, core library only needs `python-docx` + `pydantic`
- Add `[all]` extra for installing everything (`cli` + `pdf` + `watch`)
- Add unified `projects` section as alternative to split professional/personal
- Add style options: 7 fonts, 6 color themes, 3 spacing presets
- Add `json_schema()`, `to_dict()`, `sample()`, and `__repr__` to ResumeCraft
- Accept JSON strings directly in ResumeCraft constructor
- Add FastAPI and Flask usage examples in README

## v0.2.0

- Add custom section ordering via `section_order` field
- Add watch mode (`resumecraft watch`) for auto-rebuild on file changes
- Add `--open` flag to open generated file after building
- Add timestamped default output filenames
- Add PDF output support via optional `docx2pdf`

## v0.1.0

- Initial release
- JSON-driven resume generation to `.docx`
- Auto bold keywords, right-aligned dates, clickable hyperlinks
- Pydantic validation, smart page breaks
- CLI commands: `build`, `validate`, `init`
