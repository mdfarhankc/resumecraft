# ResumeCraft

[![PyPI version](https://img.shields.io/pypi/v/resumecraft.svg)](https://pypi.org/project/resumecraft/)
[![Python versions](https://img.shields.io/pypi/pyversions/resumecraft.svg)](https://pypi.org/project/resumecraft/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/resumecraft/month)](https://pepy.tech/project/resumecraft)

**Build professional Word (`.docx`) and PDF resumes from a simple JSON file.**

ResumeCraft is a Python resume/CV generator that takes JSON input and produces a polished Word document or PDF. Use it as a library, a CLI tool, or drop it into a web app (FastAPI, Flask, Django).

See the [generated PDF](examples/output/sample_resume.pdf) (built from [`sample_resume.json`](examples/sample_resume.json)) to get a feel for the formatting. Set `style.ats = true` for ATS-friendly output.

## Features

- Resume content lives in a single JSON file, easy to version control
- Auto-bolds keywords across all bullet points
- Right-aligned dates using proper tab stops
- Clickable hyperlinks for email, LinkedIn, GitHub, and projects
- Keeps section headings from getting orphaned at page breaks
- Pydantic-validated JSON input
- Custom section ordering and headings
- Sections: experience, projects (with multi-link support), skills, education, certifications, awards, languages
- Style presets: 7 fonts, 6 color themes, 3 spacing options
- Watch mode with PDF output for live preview
- Optional PDF export via `docx2pdf`
- JSON schema for editor autocomplete

## Installation

```bash
pip install resumecraft              # library + CLI
pip install resumecraft[pdf]         # + PDF export
pip install resumecraft[pdf,watch]   # + PDF export + watch mode
pip install resumecraft[all]         # everything

# Install the CLI globally
pipx install resumecraft
uv tool install resumecraft

# Or run without installing
uvx resumecraft build my-resume.json
uvx "resumecraft[all]" build my-resume.json --open
```

## Quick Start

```bash
# 1. Generate a template
resumecraft init -o my-resume.json

# 2. Edit my-resume.json with your details

# 3. Build your resume (docx)
resumecraft build my-resume.json

# 4. Build a PDF with the same filename (my-resume.pdf)
resumecraft build my-resume.json --pdf

# 5. Build and open immediately
resumecraft build my-resume.json --pdf --open

# 6. Validate without building
resumecraft validate my-resume.json

# 7. Watch for changes and rebuild automatically (defaults to PDF)
resumecraft watch my-resume.json --open
```

## CLI Reference

```
resumecraft --help                                Show all commands
resumecraft --version                             Show version
resumecraft init -o FILE                          Generate a blank JSON template
resumecraft build FILE [-o FILE] [--pdf] [--open]  Build .docx or .pdf from JSON
resumecraft validate FILE                         Validate JSON without building
resumecraft watch FILE [-o FILE] [--open]         Watch and rebuild on file changes
```

When `-o` is omitted from `build`, the output is named after the input file with a timestamp, e.g., `my-resume_2026-04-01_03-45pm.docx`.

When `-o` is omitted from `watch`, the output defaults to `<input-name>.pdf`. PDF viewers don't lock files, so changes appear instantly.

## Use as a Library

```python
from resumecraft import ResumeCraft

# Load from anywhere
rc = ResumeCraft.from_jsonfile("my-resume.json")
rc = ResumeCraft.from_yamlfile("my-resume.yaml")      # needs: pip install resumecraft[yaml]
rc = ResumeCraft.from_json('{"name": "John", ...}')   # JSON string
rc = ResumeCraft.from_yaml("name: John\n...")         # YAML string
rc = ResumeCraft.from_bytes(uploaded_bytes)           # raw bytes (uploads, request body)
rc = ResumeCraft.from_dict({"name": "John", ...})     # dict

# Export
rc.to_docx("resume.docx")            # save .docx
rc.to_pdf("resume.pdf")              # save .pdf  (needs: pip install resumecraft[pdf])
rc.to_docx_bytes()                   # docx as bytes (for streaming)
rc.to_pdf_bytes()                    # pdf as bytes
rc.to_dict()                         # back to a dict

# Discover the schema
ResumeCraft.sample()                 # sample dict with all fields
ResumeCraft.json_schema()            # JSON schema (for editor autocomplete)
```

### FastAPI example

```python
import io
from fastapi import FastAPI, UploadFile
from fastapi.responses import Response, StreamingResponse

from resumecraft import ResumeCraft

app = FastAPI()


@app.post("/resume/docx")
def generate_docx(data: dict):
    rc = ResumeCraft.from_dict(data)
    return StreamingResponse(
        io.BytesIO(rc.to_docx_bytes()),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=resume.docx"},
    )


@app.post("/resume/pdf")
def generate_pdf(data: dict):
    return Response(
        ResumeCraft.from_dict(data).to_pdf_bytes(),
        media_type="application/pdf",
    )


@app.post("/resume/upload")
async def from_upload(file: UploadFile):
    rc = ResumeCraft.from_bytes(await file.read())
    return Response(rc.to_pdf_bytes(), media_type="application/pdf")
```

### Flask example

```python
import io
from flask import Flask, request, send_file

from resumecraft import ResumeCraft

app = Flask(__name__)


@app.post("/resume/docx")
def generate_docx():
    rc = ResumeCraft.from_dict(request.json)
    return send_file(
        io.BytesIO(rc.to_docx_bytes()),
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        download_name="resume.docx",
    )


@app.post("/resume/pdf")
def generate_pdf():
    pdf = ResumeCraft.from_dict(request.json).to_pdf_bytes()
    return send_file(io.BytesIO(pdf), mimetype="application/pdf", download_name="resume.pdf")
```

See the [examples/](examples/) folder for more complete examples including Django.

### Advanced usage

The Pydantic model and the renderer are available for power users who need more control:

```python
import json
from pathlib import Path
from resumecraft.models import Resume
from resumecraft.builder import DocxBuilder

data = json.loads(Path("my-resume.json").read_text())
resume = Resume.model_validate(data)
DocxBuilder(resume).save("resume.docx")
```

## JSON Structure

Run `resumecraft init` to generate a full template. Here's the structure:

```json
{
  "$schema": "https://raw.githubusercontent.com/mdfarhankc/resumecraft/main/schema.json",
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
      "links": [
        { "label": "GitHub", "url": "https://github.com/you/project" },
        { "label": "Live Demo", "url": "https://project.example.com" }
      ],
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
  "certifications": [
    {
      "name": "AWS Certified Developer",
      "issuer": "Amazon Web Services",
      "date": "2024",
      "link": { "label": "Verify", "url": "https://aws.amazon.com/verify" }
    }
  ],
  "awards": [
    {
      "title": "Employee of the Year",
      "issuer": "Acme Corp",
      "date": "2024",
      "description": "Recognized for outstanding contributions."
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
    "certifications",
    "awards",
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
| `certifications` | object[] | No | Professional certifications with issuer, date, and optional verification link |
| `awards` | object[] | No | Awards and achievements with title, issuer, date, and optional description |
| `languages` | string | No | Language proficiencies |
| `section_order` | string[] | No | Custom order of sections (omit for default). Only listed sections are rendered. |
| `headings` | object | No | Custom section headings (e.g., `{"summary": "ABOUT ME"}`) |
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
| `ats` | `true`, `false` | `false` |

Set `"ats": true` to strip tab stops, colored tech lines, and heading borders for cleaner parsing by applicant tracking systems.

### Available sections for `section_order`

`summary`, `experience`, `projects`, `professional_projects`, `personal_projects`, `skills`, `education`, `certifications`, `awards`, `languages`

### Custom headings

Override any section's heading text:

```json
{
  "headings": {
    "summary": "ABOUT ME",
    "experience": "CAREER",
    "awards": "HONORS"
  }
}
```

### Editor autocomplete (JSON schema)

Reference the schema in your JSON for autocomplete and validation in VS Code, IntelliJ, etc.:

```json
{
  "$schema": "https://raw.githubusercontent.com/mdfarhankc/resumecraft/main/schema.json",
  "name": "Your Name",
  ...
}
```

> **Note:** Use either `projects` for a single section, or `professional_projects` + `personal_projects` for two separate sections. If you use `projects`, include it in `section_order` - it's not part of the default order.

## Project Structure

```
resumecraft/
├── pyproject.toml
├── README.md
├── CHANGELOG.md
├── LICENSE
├── Makefile
├── schema.json                 # JSON schema (regenerate with: make schema)
├── examples/
│   ├── library.py              # Library usage
│   ├── web.py                  # FastAPI/Flask/Django pattern
│   ├── sample_resume.json
│   └── output/sample_resume.pdf
├── src/resumecraft/
│   ├── __init__.py
│   ├── craft.py                # ResumeCraft (entry point)
│   ├── cli.py                  # CLI commands
│   ├── builder.py              # DocxBuilder (slim, drives the rendering)
│   ├── sections.py             # Section classes + SECTION_REGISTRY
│   ├── render.py               # RenderContext + paragraph helpers
│   ├── models.py               # Pydantic data models
│   ├── styles.py               # font/color/spacing maps
│   └── utils.py                # low-level docx helpers (hyperlinks, borders)
└── tests/
    ├── fixtures/sample.json
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
