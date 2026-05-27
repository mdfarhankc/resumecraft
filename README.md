# ResumeCraft

[![PyPI version](https://img.shields.io/pypi/v/resumecraft.svg)](https://pypi.org/project/resumecraft/)
[![Python versions](https://img.shields.io/pypi/pyversions/resumecraft.svg)](https://pypi.org/project/resumecraft/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/resumecraft/month)](https://pepy.tech/project/resumecraft)

**Generate professional resumes from JSON or YAML. Export to Word (.docx) or PDF.**

ResumeCraft takes a single data file and produces a polished, ATS-friendly resume. Use it from the command line, as a Python library, or inside a web framework like FastAPI, Flask, or Django.

**[See a sample PDF](examples/output/sample_resume.pdf)** built from [`sample_resume.json`](examples/sample_resume.json).

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [CLI Reference](#cli-reference)
- [Python Library](#python-library)
- [Resume Data Format](#resume-data-format)
  - [Minimal Example](#minimal-example)
  - [Full Example](#full-example)
  - [YAML Example](#yaml-example)
  - [Field Reference](#field-reference)
  - [Sections](#sections)
  - [Photo](#photo)
  - [Style Options](#style-options)
  - [Section Order](#section-order)
  - [Custom Headings](#custom-headings)
  - [Bold Keywords](#bold-keywords)
  - [Editor Autocomplete](#editor-autocomplete)
- [Web Framework Integration](#web-framework-integration)
- [Advanced Usage](#advanced-usage)
- [Development](#development)
- [License](#license)

---

## Installation

```bash
pip install resumecraft
```

Optional extras:

```bash
pip install resumecraft[pdf]         # PDF export (requires Microsoft Word or LibreOffice)
pip install resumecraft[yaml]        # YAML input support
pip install resumecraft[watch]       # Watch mode (rebuild on file save)
pip install resumecraft[all]         # All of the above
```

To install the CLI globally:

```bash
pipx install resumecraft
# or
uv tool install resumecraft
```

To run without installing:

```bash
uvx resumecraft build my-resume.json
uvx "resumecraft[all]" build my-resume.json --pdf --open
```

---

## Quick Start

```bash
# 1. Generate a starter template
resumecraft init -o my-resume.json

# 2. Edit my-resume.json with your details

# 3. Build a .docx resume
resumecraft build my-resume.json

# 4. Or build a PDF directly
resumecraft build my-resume.json --pdf

# 5. Build and open the result
resumecraft build my-resume.json --pdf --open

# 6. Watch for changes and rebuild on every save
resumecraft watch my-resume.json --open
```

---

## CLI Reference

```
resumecraft [--version] [--help]
resumecraft init    [-o FILE]
resumecraft build   FILE [-o FILE] [--pdf] [--open]
resumecraft validate FILE
resumecraft watch   FILE [-o FILE] [--open]
```

### `init`

Generate a blank resume JSON template with all available fields.

```bash
resumecraft init                      # creates resume-template.json
resumecraft init -o my-resume.json    # custom output path
```

### `build`

Build a `.docx` or `.pdf` resume from a JSON or YAML file.

```bash
resumecraft build my-resume.json                    # timestamped .docx
resumecraft build my-resume.json -o resume.docx     # custom filename
resumecraft build my-resume.json --pdf              # PDF (same stem as input)
resumecraft build my-resume.json -o resume.pdf      # custom PDF path
resumecraft build my-resume.json --pdf --open       # build + open
```

| Option | Description |
|---|---|
| `-o, --output FILE` | Output file path. Defaults to `<input>_YYYY-MM-DD_HH-MMam.docx` |
| `--pdf` | Output as PDF using the input file's stem. Ignored if `-o` is set |
| `--open` | Open the file after building |

### `validate`

Check a resume file for errors without building anything.

```bash
resumecraft validate my-resume.json
```

Prints field-level error messages if validation fails:

```
Error: Invalid resume data in my-resume.json
  contact.email: String should have at least 1 character
  experience.0.bullets: Field required
```

### `watch`

Watch a file and rebuild automatically on every save. Defaults to PDF output.

```bash
resumecraft watch my-resume.json              # rebuilds <input>.pdf on save
resumecraft watch my-resume.json --open       # open on first build
resumecraft watch my-resume.json -o out.docx  # output .docx instead
```

Press `Ctrl+C` to stop. Requires `pip install resumecraft[watch]`.

---

## Python Library

### Loading a Resume

```python
from resumecraft import ResumeCraft

# From files
rc = ResumeCraft.from_jsonfile("resume.json")
rc = ResumeCraft.from_yamlfile("resume.yaml")       # requires resumecraft[yaml]

# From strings
rc = ResumeCraft.from_json('{"name": "Jane", ...}')
rc = ResumeCraft.from_yaml("name: Jane\n...")        # requires resumecraft[yaml]

# From raw bytes (file uploads, HTTP request bodies)
rc = ResumeCraft.from_bytes(uploaded_file.read())

# From a Python dict
rc = ResumeCraft.from_dict({"name": "Jane", "contact": {...}, "summary": "..."})
```

### Exporting

```python
# Save to disk
rc.to_docx("resume.docx")        # returns Path
rc.to_pdf("resume.pdf")          # returns Path (requires resumecraft[pdf])

# Get bytes (for streaming responses, S3 uploads, etc.)
docx_bytes = rc.to_docx_bytes()
pdf_bytes  = rc.to_pdf_bytes()   # requires resumecraft[pdf]

# Convert back to a dict
data = rc.to_dict()
```

### Discovery Helpers

```python
# Get a complete sample resume dict (useful for templates or testing)
sample = ResumeCraft.sample()

# Get the JSON Schema (for editor autocomplete or API docs)
schema = ResumeCraft.json_schema()
```

### Full Example

```python
from resumecraft import ResumeCraft

# Load, customize, and export
rc = ResumeCraft.from_jsonfile("my-resume.json")
rc.to_docx("my-resume.docx")

# Or build from scratch
data = ResumeCraft.sample()
data["name"] = "Jane Doe"
data["style"] = {"font": "garamond", "color": "navy", "spacing": "compact"}
ResumeCraft.from_dict(data).to_pdf("jane-resume.pdf")
```

---

## Resume Data Format

ResumeCraft accepts JSON or YAML. Both formats use the same structure. All fields use strict validation - a typo like `experiance` will raise an error instead of being silently ignored.

### Minimal Example

Only three fields are required:

```json
{
  "name": "Jane Doe",
  "contact": {
    "location": "New York, NY",
    "email": "jane@example.com",
    "phone": "+1-234-567-8900"
  },
  "summary": "Full-stack developer with 5 years of experience building web applications."
}
```

### Full Example

```json
{
  "$schema": "https://raw.githubusercontent.com/mdfarhankc/resumecraft/main/schema.json",
  "name": "Jane Doe",
  "contact": {
    "location": "New York, NY",
    "email": "jane@example.com",
    "phone": "+1-234-567-8900",
    "links": [
      { "label": "LinkedIn", "url": "https://linkedin.com/in/janedoe" },
      { "label": "GitHub", "url": "https://github.com/janedoe" }
    ]
  },
  "photo": "headshot.jpg",
  "summary": "Full-stack developer with 5 years of experience building scalable web applications.",
  "bold_keywords": ["Python", "FastAPI", "React", "PostgreSQL", "AWS"],
  "experience": [
    {
      "company": "Acme Corp",
      "location": "New York, NY",
      "title": "Senior Software Engineer",
      "duration": "JAN 2022 - PRESENT",
      "bullets": [
        "Designed and deployed a FastAPI microservice handling 10K requests/sec.",
        "Led migration from monolith to microservices, reducing deploy times by 60%.",
        "Mentored 3 junior developers through code reviews and pair programming."
      ]
    }
  ],
  "projects": [
    {
      "name": "DataPipeline",
      "subtitle": "| Open Source",
      "tech_stack": "Python, Apache Kafka, PostgreSQL",
      "links": [
        { "label": "GitHub", "url": "https://github.com/janedoe/datapipeline" },
        { "label": "Docs", "url": "https://datapipeline.dev" }
      ],
      "bullets": [
        "Built a real-time data pipeline processing 1M events/day.",
        "Published as open source with 500+ GitHub stars."
      ]
    }
  ],
  "skills": [
    { "category": "Languages", "items": "Python, TypeScript, Go, SQL" },
    { "category": "Backend", "items": "FastAPI, Django, Node.js, gRPC" },
    { "category": "Infrastructure", "items": "AWS, Docker, Kubernetes, Terraform" }
  ],
  "education": [
    {
      "institution": "MIT",
      "degree": "B.S. Computer Science",
      "duration": "2016 - 2020"
    }
  ],
  "certifications": [
    {
      "name": "AWS Solutions Architect",
      "issuer": "Amazon Web Services",
      "date": "2024",
      "links": [
        { "label": "Verify", "url": "https://aws.amazon.com/verify/12345" }
      ]
    }
  ],
  "awards": [
    {
      "title": "Hack the Future - 1st Place",
      "issuer": "TechCrunch",
      "date": "2023",
      "description": "Won first place for building an AI-powered accessibility tool."
    }
  ],
  "languages": "English - Native  |  Spanish - Professional",
  "style": {
    "font": "calibri",
    "color": "navy",
    "spacing": "normal"
  },
  "section_order": [
    "summary",
    "experience",
    "projects",
    "skills",
    "education",
    "certifications",
    "awards",
    "languages"
  ],
  "headings": {
    "summary": "ABOUT ME"
  }
}
```

### YAML Example

The same resume in YAML:

```yaml
name: Jane Doe
contact:
  location: New York, NY
  email: jane@example.com
  phone: "+1-234-567-8900"
  links:
    - label: LinkedIn
      url: https://linkedin.com/in/janedoe
    - label: GitHub
      url: https://github.com/janedoe

summary: Full-stack developer with 5 years of experience.

bold_keywords:
  - Python
  - FastAPI
  - React

experience:
  - company: Acme Corp
    location: New York, NY
    title: Senior Software Engineer
    duration: JAN 2022 - PRESENT
    bullets:
      - Designed and deployed a FastAPI microservice handling 10K requests/sec.
      - Led migration from monolith to microservices, reducing deploy times by 60%.

skills:
  - category: Languages
    items: Python, TypeScript, Go, SQL
  - category: Backend
    items: FastAPI, Django, Node.js, gRPC

education:
  - institution: MIT
    degree: B.S. Computer Science
    duration: 2016 - 2020

style:
  font: garamond
  color: forest
  spacing: compact
```

Requires `pip install resumecraft[yaml]`.

### Field Reference

#### Resume (top-level)

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `name` | string | **Yes** | | Full name at the top of the resume |
| `contact` | Contact | **Yes** | | Location, email, phone, and links |
| `summary` | string | **Yes** | | Professional summary paragraph |
| `photo` | string | No | `null` | Path or URL to a profile photo |
| `bold_keywords` | string[] | No | `[]` | Words auto-bolded in all bullet points |
| `experience` | Experience[] | No | `[]` | Work experience entries |
| `projects` | Project[] | No | `[]` | Unified projects section |
| `professional_projects` | Project[] | No | `[]` | Professional/client projects |
| `personal_projects` | Project[] | No | `[]` | Side projects and open source |
| `skills` | Skill[] | No | `[]` | Categorized skill lists |
| `education` | Education[] | No | `[]` | Degrees and institutions |
| `certifications` | Certification[] | No | `[]` | Certifications with optional links |
| `awards` | Award[] | No | `[]` | Awards with optional description |
| `languages` | string | No | `""` | Language proficiencies (free text) |
| `section_order` | string[] | No | `null` | Controls which sections appear and in what order |
| `headings` | object | No | `{}` | Override default section heading text |
| `style` | StyleOptions | No | `{}` | Font, color, spacing, and ATS settings |
| `$schema` | string | No | | Editor autocomplete hint (ignored at runtime) |
| `_version` | string | No | | ResumeCraft version (ignored at runtime) |

#### Contact

| Field | Type | Required | Description |
|---|---|---|---|
| `location` | string | **Yes** | City, state/country |
| `email` | string | **Yes** | Email address (rendered as a `mailto:` link) |
| `phone` | string | **Yes** | Phone number |
| `links` | Link[] | No | Additional links (LinkedIn, GitHub, portfolio, etc.) |

#### Link

| Field | Type | Required | Description |
|---|---|---|---|
| `label` | string | **Yes** | Display text (e.g., "LinkedIn", "GitHub") |
| `url` | string | **Yes** | Full URL |

#### Experience

| Field | Type | Required | Description |
|---|---|---|---|
| `company` | string | **Yes** | Company name |
| `location` | string | **Yes** | City, country or "Remote" |
| `title` | string | **Yes** | Job title |
| `duration` | string | **Yes** | Time period (e.g., `"JAN 2022 - PRESENT"`) |
| `bullets` | string[] | **Yes** | Accomplishments and responsibilities |

#### Project

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | **Yes** | Project name |
| `subtitle` | string | **Yes** | Short description (e.g., `"\| Open Source"`) |
| `tech_stack` | string | No | Technologies used (rendered in italic) |
| `links` | Link[] | No | Project links (GitHub, live demo, docs) |
| `bullets` | string[] | **Yes** | What you built and the impact |

#### Skill

| Field | Type | Required | Description |
|---|---|---|---|
| `category` | string | **Yes** | Skill group name (e.g., "Backend", "DevOps") |
| `items` | string | **Yes** | Comma-separated skills |

#### Education

| Field | Type | Required | Description |
|---|---|---|---|
| `institution` | string | **Yes** | University or school name |
| `degree` | string | **Yes** | Degree and field of study |
| `duration` | string | **Yes** | Time period (e.g., `"2016 - 2020"`) |

#### Certification

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | **Yes** | Certification name |
| `issuer` | string | **Yes** | Issuing organization |
| `date` | string | **Yes** | Year or date obtained |
| `links` | Link[] | No | Verification or credential links |

#### Award

| Field | Type | Required | Description |
|---|---|---|---|
| `title` | string | **Yes** | Award name |
| `issuer` | string | **Yes** | Awarding organization |
| `date` | string | **Yes** | Year received |
| `description` | string | No | Brief description of the award |

### Sections

ResumeCraft supports 10 section types:

| Section | Default Heading | Description |
|---|---|---|
| `summary` | PROFESSIONAL SUMMARY | A paragraph about your background |
| `experience` | WORK EXPERIENCE | Jobs with company, title, duration, and bullets |
| `projects` | PROJECTS | Unified projects section |
| `professional_projects` | PROFESSIONAL PROJECTS | Work-related projects (use with `personal_projects`) |
| `personal_projects` | PERSONAL & OPEN SOURCE PROJECTS | Side projects and open source |
| `skills` | SKILLS | Categorized skill lists |
| `education` | EDUCATION | Degrees and institutions |
| `certifications` | CERTIFICATIONS | Professional certifications |
| `awards` | AWARDS & ACHIEVEMENTS | Awards and honors |
| `languages` | LANGUAGES | Language proficiencies |

Use either `projects` for a single section, or `professional_projects` + `personal_projects` for two separate sections.

Empty sections are automatically skipped.

### Photo

Add a profile photo to the header. The photo appears on the left with your name and contact info on the right.

```json
{
  "photo": "headshot.jpg"
}
```

Accepts a local file path or a URL:

```json
{ "photo": "/path/to/photo.png" }
{ "photo": "https://example.com/photo.jpg" }
```

The photo is rendered at 1 inch square. In ATS mode (`"ats": true`), the photo is skipped entirely since ATS parsers cannot process images. When no photo is provided, the header uses a centered layout.

Supported formats: PNG, JPEG, GIF, BMP, TIFF.

### Style Options

Customize the look of your resume with the `style` object:

```json
{
  "style": {
    "font": "garamond",
    "color": "navy",
    "spacing": "compact",
    "ats": false
  }
}
```

#### Fonts

| Value | Font |
|---|---|
| `calibri` | Calibri (default) |
| `arial` | Arial |
| `times` | Times New Roman |
| `garamond` | Garamond |
| `georgia` | Georgia |
| `helvetica` | Helvetica |
| `cambria` | Cambria |

#### Color Themes

| Value | Description |
|---|---|
| `black` | Classic black headings with blue links (default) |
| `navy` | Dark blue headings and links |
| `forest` | Dark green headings and links |
| `maroon` | Deep red headings and links |
| `slate` | Dark gray headings and links |
| `royal` | Deep purple headings and links |

#### Spacing Presets

| Value | Description |
|---|---|
| `compact` | Tight spacing - fits more content on a page |
| `normal` | Balanced spacing (default) |
| `relaxed` | More breathing room between sections |

#### ATS Mode

Set `"ats": true` to produce output optimized for Applicant Tracking Systems:

- Removes tab stops (uses inline separators instead)
- Removes colored text on tech stack lines
- Removes decorative heading borders
- Skips the profile photo
- Adds a "Tech:" prefix to tech stack lines for clarity

### Section Order

Control which sections appear and in what order using `section_order`. Only listed sections are rendered.

```json
{
  "section_order": ["summary", "skills", "experience", "education"]
}
```

When omitted, all non-empty sections render in the default order: summary, experience, projects, professional_projects, personal_projects, skills, education, certifications, awards, languages.

### Custom Headings

Override any section's default heading text:

```json
{
  "headings": {
    "summary": "ABOUT ME",
    "experience": "CAREER HISTORY",
    "skills": "TECHNICAL SKILLS",
    "awards": "HONORS & RECOGNITION"
  }
}
```

### Bold Keywords

List words that should be automatically bolded wherever they appear in bullet points:

```json
{
  "bold_keywords": ["Python", "FastAPI", "React", "PostgreSQL", "AWS"]
}
```

Longer keywords are matched first to avoid partial matches (e.g., "REST API" matches before "API"). Special characters like `C++` and `Node.js` are handled correctly.

### Editor Autocomplete

Add a `$schema` reference for autocomplete and validation in VS Code, IntelliJ, and other editors:

```json
{
  "$schema": "https://raw.githubusercontent.com/mdfarhankc/resumecraft/main/schema.json",
  "name": "Your Name"
}
```

The `$schema` and `_version` keys are silently ignored during validation.

---

## Web Framework Integration

ResumeCraft's factory methods and byte exports are designed for web APIs.

### FastAPI

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


@app.get("/resume/sample")
def sample():
    return ResumeCraft.sample()


@app.get("/resume/schema")
def schema():
    return ResumeCraft.json_schema()
```

### Flask

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

### Django

```python
from django.http import HttpResponse

from resumecraft import ResumeCraft


def generate_docx(request):
    import json
    data = json.loads(request.body)
    rc = ResumeCraft.from_dict(data)
    response = HttpResponse(
        rc.to_docx_bytes(),
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    response["Content-Disposition"] = "attachment; filename=resume.docx"
    return response
```

See the [examples/](examples/) folder for runnable examples.

---

## Advanced Usage

### Direct Model and Builder Access

For full control over the document, use the Pydantic model and builder directly:

```python
import json
from pathlib import Path

from resumecraft.builder import DocxBuilder
from resumecraft.models import Resume

data = json.loads(Path("my-resume.json").read_text())
resume = Resume.model_validate(data)

builder = DocxBuilder(resume)
doc = builder.build()     # returns a python-docx Document object
builder.save("resume.docx")
```

### Programmatic Resume Construction

```python
from resumecraft import ResumeCraft
from resumecraft.models import Contact, Experience, Resume, Skill

resume = Resume(
    name="Jane Doe",
    contact=Contact(
        location="New York, NY",
        email="jane@example.com",
        phone="+1-234-567-8900",
    ),
    summary="Senior software engineer with 8 years of experience.",
    experience=[
        Experience(
            company="Acme Corp",
            location="New York, NY",
            title="Staff Engineer",
            duration="JAN 2020 - PRESENT",
            bullets=[
                "Architected a distributed event processing system.",
                "Reduced infrastructure costs by 40% through optimization.",
            ],
        ),
    ],
    skills=[
        Skill(category="Languages", items="Python, Go, TypeScript"),
        Skill(category="Infrastructure", items="AWS, Kubernetes, Terraform"),
    ],
)

rc = ResumeCraft(resume)
rc.to_docx("jane-doe.docx")
```

---

## Development

```bash
git clone https://github.com/mdfarhankc/resumecraft.git
cd resumecraft
uv sync --extra dev
```

```bash
uv run pytest                       # run tests
uv run ruff check src/ tests/       # lint
uv run mypy src/                    # type check
uv build                            # build wheel + sdist
```

Tag a GitHub release (e.g., `v0.7.0`) and the CI workflow publishes to PyPI automatically via trusted publishing.

---

## License

MIT
