# ResumeCraft

A Python CLI tool and library that generates professionally formatted `.docx` resumes from JSON data. Define your resume content in a simple JSON file and get a polished Word document with proper formatting — right-aligned dates, bold keyword highlighting, clickable hyperlinks, and clean page breaks.

## Features

- **JSON-driven** — All resume content lives in a single JSON file, easy to version control
- **Auto bold keywords** — Define a list of keywords and they get bolded automatically in all bullet points
- **Right-aligned dates** — Company locations and durations are properly right-aligned using tab stops
- **Clickable hyperlinks** — Email, LinkedIn, GitHub, and project links are real clickable hyperlinks
- **Smart page breaks** — Section headers never get orphaned at the bottom of a page
- **Separate project sections** — Professional projects and personal/open source projects in distinct sections
- **Tech stack tags** — Italic grey tech stack line under each project
- **Pydantic validation** — JSON is validated against strict data models before building
- **PDF output** — Optional PDF conversion via `docx2pdf`

## Installation

### From PyPI

```bash
pip install resumecraft
```

With PDF support:

```bash
pip install resumecraft[pdf]
```

### As a CLI tool (recommended)

```bash
pipx install resumecraft
# or
uv tool install resumecraft
```

## Quick Start

```bash
# 1. Generate a template
resumecraft init -o my-resume.json

# 2. Edit my-resume.json with your details

# 3. Build your resume
resumecraft build my-resume.json -o resume.docx

# 4. Validate without building
resumecraft validate my-resume.json
```

## CLI Reference

```
resumecraft --help              Show all commands
resumecraft --version           Show version
resumecraft init -o FILE        Generate a blank JSON template
resumecraft build FILE -o FILE  Build .docx (or .pdf) from JSON
resumecraft validate FILE       Validate JSON without building
```

## Use as a Library

```python
from resumecraft import Resume, DocxBuilder

# From JSON file
resume = Resume.from_json("my-resume.json")
DocxBuilder(resume).save("resume.docx")

# Or build the model directly
from resumecraft.models import Resume, Contact, Link, Experience

resume = Resume(
    name="John Doe",
    contact=Contact(
        location="New York, NY",
        email="john@example.com",
        phone="+1-234-567-8900",
        links=[Link(label="GitHub", url="https://github.com/johndoe")],
    ),
    summary="Software engineer with 5 years of experience...",
    bold_keywords=["Python", "React", "FastAPI"],
    experience=[
        Experience(
            company="Acme Corp",
            location="New York, NY",
            title="Senior Developer",
            duration="JAN 2022 - PRESENT",
            bullets=["Built APIs using FastAPI and PostgreSQL."],
        )
    ],
)
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
  "languages": "English - Native  |  Hindi - Professional"
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
| `professional_projects` | object[] | No | Client/employer projects |
| `personal_projects` | object[] | No | Side projects and open source work |
| `skills` | object[] | No | Categorized skill lists |
| `education` | object[] | No | Degrees and institutions |
| `languages` | string | No | Language proficiencies |

## Project Structure

```
resumecraft/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/resumecraft/
│   ├── __init__.py        # Public API (Resume, DocxBuilder)
│   ├── cli.py             # Typer CLI commands (build, validate, init)
│   ├── models.py          # Pydantic data models
│   ├── builder.py         # DocxBuilder — converts models to .docx
│   ├── styles.py          # Styling constants (fonts, sizes, colors, margins)
│   └── utils.py           # Helpers (hyperlinks, keep_with_next, bold patterns)
└── tests/
    ├── fixtures/
    │   └── sample.json    # Sample resume for tests
    ├── test_models.py
    ├── test_builder.py
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

```bash
uv publish
```

You'll need a [PyPI API token](https://pypi.org/manage/account/token/).

## License

MIT
