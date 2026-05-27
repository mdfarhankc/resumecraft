# Advanced Usage

## Direct Model Access

For full control, use the Pydantic models and builder directly:

```python
import json
from pathlib import Path

from resumecraft.builder import DocxBuilder
from resumecraft.models import Resume

data = json.loads(Path("my-resume.json").read_text())
resume = Resume.model_validate(data)

# Access the python-docx Document object
builder = DocxBuilder(resume)
doc = builder.build()

# Inspect or modify the document before saving
print(f"Paragraphs: {len(doc.paragraphs)}")
print(f"Tables: {len(doc.tables)}")

builder.save("resume.docx")
```

---

## Programmatic Construction

Build a resume entirely in Python without any JSON or YAML:

```python
from resumecraft import ResumeCraft
from resumecraft.models import (
    Award,
    Certification,
    Contact,
    Education,
    Experience,
    Link,
    Project,
    Resume,
    Skill,
    StyleOptions,
)

resume = Resume(
    name="Jane Doe",
    contact=Contact(
        location="New York, NY",
        email="jane@example.com",
        phone="+1-234-567-8900",
        links=[
            Link(label="LinkedIn", url="https://linkedin.com/in/janedoe"),
            Link(label="GitHub", url="https://github.com/janedoe"),
        ],
    ),
    summary="Senior software engineer with 8 years of experience.",
    bold_keywords=["Python", "FastAPI", "AWS"],
    experience=[
        Experience(
            company="Acme Corp",
            location="New York, NY",
            title="Staff Engineer",
            duration="JAN 2020 - PRESENT",
            bullets=[
                "Architected a distributed event processing system using Python and AWS.",
                "Reduced infrastructure costs by 40% through optimization.",
            ],
        ),
    ],
    skills=[
        Skill(category="Languages", items="Python, Go, TypeScript"),
        Skill(category="Infrastructure", items="AWS, Kubernetes, Terraform"),
    ],
    education=[
        Education(
            institution="MIT",
            degree="M.S. Computer Science",
            duration="2014 - 2016",
        ),
    ],
    style=StyleOptions(font="garamond", color="navy", spacing="compact"),
    section_order=["summary", "experience", "skills", "education"],
)

rc = ResumeCraft(resume)
rc.to_docx("jane-doe.docx")
```

---

## Validation Only

Validate data without building a document:

```python
from pydantic import ValidationError
from resumecraft.models import Resume

data = {"name": "Jane", "contact": {"location": "", "email": "x", "phone": ""}}

try:
    Resume.model_validate(data)
except ValidationError as e:
    for error in e.errors():
        loc = ".".join(str(p) for p in error["loc"])
        print(f"  {loc}: {error['msg']}")
```

Output:

```
  contact.location: String should have at least 1 character
  contact.phone: String should have at least 1 character
  summary: Field required
```

---

## Generating a JSON Schema

Generate the schema for editor autocomplete or API documentation:

```python
import json
from resumecraft import ResumeCraft

schema = ResumeCraft.json_schema()
print(json.dumps(schema, indent=2))
```

Or from the command line:

```bash
python -c "
from resumecraft.models import Resume
import json
print(json.dumps(Resume.model_json_schema(), indent=2))
" > schema.json
```

---

## Roundtripping

Export and reimport without data loss:

```python
from resumecraft import ResumeCraft

rc1 = ResumeCraft.from_jsonfile("resume.json")
data = rc1.to_dict()

# Modify in Python
data["style"]["color"] = "navy"
data["bold_keywords"].append("Terraform")

rc2 = ResumeCraft.from_dict(data)
rc2.to_docx("updated-resume.docx")
```
