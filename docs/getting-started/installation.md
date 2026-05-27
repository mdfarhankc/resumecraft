# Installation

## Basic Install

```bash
pip install resumecraft
```

This installs the core library and CLI with DOCX export support.

## Optional Extras

ResumeCraft keeps optional dependencies separate so you only install what you need.

| Extra | Command | What it adds |
|---|---|---|
| `pdf` | `pip install resumecraft[pdf]` | PDF export via [docx2pdf](https://pypi.org/project/docx2pdf/) |
| `yaml` | `pip install resumecraft[yaml]` | YAML input support via [PyYAML](https://pypi.org/project/PyYAML/) |
| `watch` | `pip install resumecraft[watch]` | Watch mode via [watchfiles](https://pypi.org/project/watchfiles/) |
| `all` | `pip install resumecraft[all]` | All of the above |

!!! note "PDF export requirements"
    `docx2pdf` requires **Microsoft Word** (Windows/macOS) or **LibreOffice** (Linux) to be installed on the system. It converts `.docx` to `.pdf` using the application's built-in converter.

## Global CLI Install

To use `resumecraft` as a system-wide command without activating a virtual environment:

=== "pipx"

    ```bash
    pipx install resumecraft
    pipx install "resumecraft[all]"     # with all extras
    ```

=== "uv"

    ```bash
    uv tool install resumecraft
    uv tool install "resumecraft[all]"  # with all extras
    ```

## Run Without Installing

```bash
uvx resumecraft build my-resume.json
uvx "resumecraft[all]" build my-resume.json --pdf --open
```

## Requirements

- Python **3.10** or newer
- Tested on Python 3.10, 3.11, 3.12, 3.13, and 3.14
- Works on Windows, macOS, and Linux

## Core Dependencies

These are installed automatically:

| Package | Purpose |
|---|---|
| [python-docx](https://python-docx.readthedocs.io/) | Word document generation |
| [Pydantic](https://docs.pydantic.dev/) | Data validation with strict mode |
| [Typer](https://typer.tiangolo.com/) | CLI framework |
