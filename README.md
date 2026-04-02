# ResumeCraft

A Python library and CLI tool that generates professionally formatted `.docx` resumes from JSON data. Define your resume content in a simple JSON file and get a polished Word document with proper formatting — right-aligned dates, bold keyword highlighting, clickable hyperlinks, and clean page breaks.

Use it standalone, as a CLI tool, or integrate it into your web app (FastAPI, Django, Flask, etc.).

## Features

- **JSON-driven** — All resume content lives in a single JSON file, easy to version control
- **Auto bold keywords** — Define a list of keywords and they get bolded automatically in all bullet points
- **Right-aligned dates** — Company locations and durations are properly right-aligned using tab stops
- **Clickable hyperlinks** — Email, LinkedIn, GitHub, and project links are real clickable hyperlinks
- **Smart page breaks** — Section headers never get orphaned at the bottom of a page
- **Separate project sections** — Professional projects and personal/open source projects in distinct sections
- **Tech stack tags** — Italic grey tech stack line under each project
- **Pydantic validation** — JSON is validated against strict data models before building
- **Custom section ordering** — Control which sections appear and in what order
- **Watch mode** — Auto-rebuild on file save
- **PDF output** — Optional PDF conversion via `docx2pdf`
- **Auto-open** — Open the generated file after building with `--open`

## Installation

### As a library

```bash
pip install resumecraft                # Core library only
pip install resumecraft[pdf]           # + PDF output support
```

### As a CLI tool

```bash
pip install resumecraft[cli]           # Core + CLI
pip install resumecraft[cli,pdf,watch] # Everything
pip install resumecraft[all]           # Same as above

# Or install globally
pipx install "resumecraft[cli]"
uv tool install "resumecraft[cli]"
```

## Quick Start

```bash
# 1. Generate a template
resumecraft init -o my-resume.json

# 2. Edit my-resume.json with your details

# 3. Build your resume
resumecraft build my-resume.json

# 4. Build and open immediately
resumecraft build my-resume.json --open

# 5. Validate without building
resumecraft validate my-resume.json

# 6. Watch for changes and rebuild automatically
resumecraft watch my-resume.json -o resume.docx
```

## CLI Reference

```
resumecraft --help                      Show all commands
resumecraft --version                   Show version
resumecraft init -o FILE                Generate a blank JSON template
resumecraft build FILE [-o FILE] [--open]  Build .docx (or .pdf) from JSON
resumecraft validate FILE               Validate JSON without building
resumecraft watch FILE [-o FILE]        Watch and rebuild on file changes
```

When `-o` is omitted from `build`, the output file is automatically named with a timestamp, e.g., `resume_2026-04-01_03-45pm.docx`.

## Use as a Library

```python
from resumecraft import ResumeCraft

# From a JSON file
rc = ResumeCraft.from_json("my-resume.json")
rc.to_docx("resume.docx")

# From a dict
rc = ResumeCraft({"name": "John Doe", "contact": {...}, "summary": "..."})
rc.to_docx("resume.docx")

# From a JSON string
rc = ResumeCraft('{"name": "John Doe", ...}')

# Get bytes (for web frameworks)
content = rc.to_bytes()

# Export as PDF (requires: pip install resumecraft[pdf])
rc.to_pdf("resume.pdf")

# Export back to dict
data = rc.to_dict()

# Get a sample template to see all fields
sample = ResumeCraft.sample()

# Get JSON schema for editor validation
schema = ResumeCraft.json_schema()
```

### FastAPI example

```python
import io
import tempfile
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from resumecraft import ResumeCraft

app = FastAPI()

@app.post("/resume/docx")
def generate_docx(data: dict):
    rc = ResumeCraft(data)
    return StreamingResponse(
        io.BytesIO(rc.to_bytes()),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=resume.docx"},
    )

@app.post("/resume/pdf")
def generate_pdf(data: dict):
    rc = ResumeCraft(data)
    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    rc.to_pdf(tmp.name)
    return FileResponse(tmp.name, filename="resume.pdf", media_type="application/pdf")
```

### Flask example

```python
import io
import tempfile
from flask import Flask, request, send_file
from resumecraft import ResumeCraft

app = Flask(__name__)

@app.post("/resume/docx")
def generate_docx():
    rc = ResumeCraft(request.json)
    return send_file(
        io.BytesIO(rc.to_bytes()),
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        download_name="resume.docx",
    )

@app.post("/resume/pdf")
def generate_pdf():
    rc = ResumeCraft(request.json)
    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    rc.to_pdf(tmp.name)
    return send_file(tmp.name, mimetype="application/pdf", download_name="resume.pdf")
```

### Advanced usage

You can also use the lower-level `Resume` and `DocxBuilder` classes directly:

```python
from resumecraft import Resume, DocxBuilder

resume = Resume.from_json("my-resume.json")
DocxBuilder(resume).save("resume.docx")
```

## JSON Structure

Run `resumecraft init` to generate a full template. Here's the structure:

```json
{
  "name": "Your Name",
  "contact": {
    "location": "City, Country",
    "email": "your@email.com",
    "phone": "+1-234-567-8900",
    "links": [
      { "label": "LinkedIn", "url": "https://linkedin.com/in/you" },
      { "label": "GitHub", "url": "https://github.com/you" }
    ]
  },
  "summary": "A brief professional summary...",
  "bold_keywords": ["FastAPI", "React", "PostgreSQL"],
  "experience": [
    {
      "company": "Company Name",
      "location": "City, Country",
      "title": "Your Title",
      "duration": "JAN 2023 - PRESENT",
      "bullets": ["What you did and the impact it had."]
    }
  ],
  "projects": [
    {
      "name": "Project Name",
      "subtitle": "| Description",
      "tech_stack": "Python, FastAPI",
      "link": null,
      "bullets": ["What you built."]
    }
  ],
  "professional_projects": [
    {
      "name": "Project Name",
      "subtitle": "| Location | Type",
      "tech_stack": "FastAPI, React, PostgreSQL",
      "link": null,
      "bullets": ["What you built."]
    }
  ],
  "personal_projects": [
    {
      "name": "Side Project",
      "subtitle": "| Personal Project",
      "tech_stack": null,
      "link": { "label": "GitHub", "url": "https://github.com/you/project" },
      "bullets": ["What you built and why."]
    }
  ],
  "skills": [
    { "category": "Backend", "items": "Python (FastAPI, Django), Node.js" },
    { "category": "Frontend", "items": "React, TypeScript" }
  ],
  "education": [
    {
      "institution": "University Name",
      "degree": "Bachelor of Computer Science",
      "duration": "2019 - 2023"
    }
  ],
  "languages": "English - Native  |  Hindi - Professional",
  "style": {
    "font": "calibri",
    "color": "black",
    "spacing": "normal"
  },
  "section_order": [
    "summary",
    "experience",
    "professional_projects",
    "personal_projects",
    "skills",
    "education",
    "languages"
  ]
}
```

### Field Reference

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | Full name displayed at the top |
| `contact` | object | Yes | Location, email, phone, and links |
| `summary` | string | Yes | Professional summary paragraph |
| `bold_keywords` | string[] | No | Words to auto-bold in all bullet points |
| `experience` | object[] | No | Work experience entries |
| `projects` | object[] | No | Single unified projects section |
| `professional_projects` | object[] | No | Client/employer projects (use with `personal_projects` for split sections) |
| `personal_projects` | object[] | No | Side projects and open source work |
| `skills` | object[] | No | Categorized skill lists |
| `education` | object[] | No | Degrees and institutions |
| `languages` | string | No | Language proficiencies |
| `section_order` | string[] | No | Custom order of sections (omit for default). Only listed sections are rendered. |
| `style` | object | No | Styling options (font, color, spacing) |

### Style Options

Add a `style` object to customize the look of your resume:

```json
{
  "style": {
    "font": "garamond",
    "color": "navy",
    "spacing": "compact"
  }
}
```

| Option | Choices | Default |
|--------|---------|---------|
| `font` | `calibri`, `arial`, `times`, `garamond`, `georgia`, `helvetica`, `cambria` | `calibri` |
| `color` | `black`, `navy`, `forest`, `maroon`, `slate`, `royal` | `black` |
| `spacing` | `compact`, `normal`, `relaxed` | `normal` |

### Available sections for `section_order`

`summary`, `experience`, `projects`, `professional_projects`, `personal_projects`, `skills`, `education`, `languages`

> **Note:** Use either `projects` for a single section, or `professional_projects` + `personal_projects` for two separate sections. If you use `projects`, include it in `section_order` — it's not part of the default order.

## Project Structure

```
resumecraft/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/resumecraft/
│   ├── __init__.py        # Public API (ResumeCraft, Resume, DocxBuilder)
│   ├── craft.py           # ResumeCraft facade (simple high-level API)
│   ├── cli.py             # Typer CLI commands (build, validate, init, watch)
│   ├── models.py          # Pydantic data models
│   ├── builder.py         # DocxBuilder — converts models to .docx
│   ├── styles.py          # Styling constants (fonts, sizes, colors, margins)
│   └── utils.py           # Helpers (hyperlinks, keep_with_next, bold patterns)
└── tests/
    ├── fixtures/
    │   └── sample.json    # Sample resume for tests
    ├── test_models.py
    ├── test_builder.py
    ├── test_craft.py
    ├── test_cli.py
    └── test_utils.py
```

## Development

```bash
git clone https://github.com/mdfarhankc/resumecraft.git
cd resumecraft
uv sync --extra dev
```

### Run tests

```bash
uv run pytest
```

### Build

```bash
uv build
```

This creates `dist/resumecraft-x.x.x.tar.gz` and `dist/resumecraft-x.x.x-py3-none-any.whl`.

### Publish to PyPI

Create a GitHub release (e.g., `v0.2.0`) and the CI workflow will publish to PyPI automatically via trusted publishing.

## License

MIT
