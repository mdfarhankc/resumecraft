# CLI Reference

## Global Options

```bash
resumecraft --version    # Show version and exit
resumecraft -v           # Short form
resumecraft --help       # Show all commands
```

---

## `init`

Generate a blank resume JSON template with every available field.

```bash
resumecraft init [-o FILE]
```

| Option | Default | Description |
|---|---|---|
| `-o, --output` | `resume-template.json` | Output file path |

**Examples:**

```bash
resumecraft init                        # creates resume-template.json
resumecraft init -o my-resume.json      # custom path
resumecraft init -o drafts/v2.json      # creates parent dirs automatically
```

The generated template includes a `$schema` reference for editor autocomplete and a `_version` field. Both are ignored during validation.

---

## `build`

Build a `.docx` or `.pdf` resume from a JSON or YAML file.

```bash
resumecraft build FILE [-o FILE] [--pdf] [--open]
```

| Argument / Option | Default | Description |
|---|---|---|
| `FILE` (required) | | Input `.json`, `.yaml`, or `.yml` file |
| `-o, --output` | auto-generated | Output file path |
| `--pdf` | `false` | Output as PDF using the input file's stem |
| `--open` | `false` | Open the file after building |

**Default output filename:**

When `-o` is omitted, the output is named after the input file with a timestamp:

```
my-resume_2026-05-26_03-45pm.docx
```

When `--pdf` is used without `-o`, the output uses the input stem:

```
my-resume.pdf
```

**Examples:**

```bash
# Default timestamped .docx
resumecraft build my-resume.json

# Custom output path
resumecraft build my-resume.json -o resume.docx

# PDF output
resumecraft build my-resume.json --pdf
resumecraft build my-resume.json -o resume.pdf

# Build and open
resumecraft build my-resume.json --pdf --open

# YAML input
resumecraft build my-resume.yaml -o resume.docx
```

!!! note "PDF requirements"
    PDF output requires `pip install resumecraft[pdf]` and Microsoft Word or LibreOffice.

---

## `validate`

Check a resume file for errors without building anything.

```bash
resumecraft validate FILE
```

| Argument | Description |
|---|---|
| `FILE` (required) | Input `.json`, `.yaml`, or `.yml` file |

**Examples:**

```bash
resumecraft validate my-resume.json
# Valid: my-resume.json

resumecraft validate broken.json
# Error: Invalid resume data in broken.json
#   contact: Field required
#   summary: Field required
```

Validation catches:

- Missing required fields
- Unknown field names (strict mode rejects typos)
- Invalid values for `style.font`, `style.color`, `style.spacing`
- Duplicate entries in `section_order`
- Invalid section names in `section_order` or `headings`
- Malformed JSON/YAML syntax
- Non-UTF-8 file encoding

---

## `watch`

Watch a file and rebuild automatically on every save.

```bash
resumecraft watch FILE [-o FILE] [--open]
```

| Argument / Option | Default | Description |
|---|---|---|
| `FILE` (required) | | Input `.json`, `.yaml`, or `.yml` file |
| `-o, --output` | `<input>.pdf` | Output file path |
| `--open` | `false` | Open the file after the first build |

Watch mode defaults to PDF output because most PDF viewers automatically reload when the file changes, giving you a live preview.

**Examples:**

```bash
# Watch and rebuild as PDF (default)
resumecraft watch my-resume.json

# Watch, build, and open
resumecraft watch my-resume.json --open

# Watch and output .docx instead
resumecraft watch my-resume.json -o resume.docx
```

Press `Ctrl+C` to stop watching.

!!! info "Error recovery"
    If a rebuild fails (invalid JSON, missing fields), watch mode prints the error and waits for the next save. If the output file is locked (e.g., open in Word), it retries on the next change.

Requires `pip install resumecraft[watch]`.

---

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | Success |
| `1` | Error (file not found, invalid data, missing dependency, etc.) |

All error messages are printed to stderr with clear descriptions and suggestions.
