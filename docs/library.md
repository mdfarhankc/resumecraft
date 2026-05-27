# Python Library

## Overview

The main entry point is the `ResumeCraft` class, available from the top-level package:

```python
from resumecraft import ResumeCraft
```

The typical workflow is: **load** data via a factory method, then **export** to a file or bytes.

---

## Loading Data

### From Files

```python
rc = ResumeCraft.from_jsonfile("resume.json")
rc = ResumeCraft.from_yamlfile("resume.yaml")   # requires resumecraft[yaml]
```

Both methods handle UTF-8 BOM encoding automatically.

### From Strings

```python
rc = ResumeCraft.from_json('{"name": "Jane", "contact": {...}, "summary": "..."}')
rc = ResumeCraft.from_yaml("name: Jane\ncontact:\n  ...")  # requires resumecraft[yaml]
```

### From Bytes

Useful for file uploads and HTTP request bodies:

```python
rc = ResumeCraft.from_bytes(uploaded_file.read())
```

Handles UTF-8 and UTF-8 BOM. Raises `ValueError` for non-UTF-8 input with a clear message.

### From a Dict

```python
rc = ResumeCraft.from_dict({
    "name": "Jane Doe",
    "contact": {
        "location": "New York, NY",
        "email": "jane@example.com",
        "phone": "+1-234-567-8900",
    },
    "summary": "Full-stack developer with 5 years of experience.",
})
```

### From a Resume Model

For programmatic construction using Pydantic models directly:

```python
from resumecraft.models import Contact, Resume

resume = Resume(
    name="Jane Doe",
    contact=Contact(location="NYC", email="jane@example.com", phone="+1-234-567-8900"),
    summary="Full-stack developer.",
)
rc = ResumeCraft(resume)
```

---

## Exporting

### To Files

```python
path = rc.to_docx("resume.docx")   # returns Path
path = rc.to_pdf("resume.pdf")     # returns Path (requires resumecraft[pdf])
```

Both methods create parent directories automatically.

### To Bytes

For streaming responses, S3 uploads, or any in-memory use:

```python
docx_bytes = rc.to_docx_bytes()    # bytes (ZIP/DOCX format)
pdf_bytes  = rc.to_pdf_bytes()     # bytes (requires resumecraft[pdf])
```

### To Dict

```python
data = rc.to_dict()   # dict[str, Any]
```

Returns the validated resume data as a plain dictionary. Useful for serialization or roundtripping.

---

## Discovery Helpers

### Sample Data

Get a complete resume dictionary with every field populated:

```python
sample = ResumeCraft.sample()
```

Useful for generating templates, testing, or exploring the schema.

### JSON Schema

Get the Pydantic-generated JSON Schema:

```python
schema = ResumeCraft.json_schema()
```

Useful for API documentation, editor autocomplete, or client-side validation.

---

## Error Handling

All factory methods raise standard exceptions:

| Exception | When |
|---|---|
| `pydantic.ValidationError` | Invalid or missing fields in the resume data |
| `json.JSONDecodeError` | Malformed JSON string |
| `ValueError` | Non-UTF-8 bytes, invalid photo path/URL |
| `FileNotFoundError` | Input file doesn't exist |
| `ImportError` | Missing optional dependency (`pyyaml`, `docx2pdf`) |

```python
from pydantic import ValidationError

try:
    rc = ResumeCraft.from_dict({"name": "Jane"})  # missing contact and summary
except ValidationError as e:
    for error in e.errors():
        print(f"{error['loc']}: {error['msg']}")
```

---

## API Summary

### Factory Methods

| Method | Input | Returns |
|---|---|---|
| `ResumeCraft.from_jsonfile(path)` | File path (str or Path) | `ResumeCraft` |
| `ResumeCraft.from_yamlfile(path)` | File path (str or Path) | `ResumeCraft` |
| `ResumeCraft.from_json(text)` | JSON string | `ResumeCraft` |
| `ResumeCraft.from_yaml(text)` | YAML string | `ResumeCraft` |
| `ResumeCraft.from_bytes(data)` | Raw bytes | `ResumeCraft` |
| `ResumeCraft.from_dict(data)` | Dict or Mapping | `ResumeCraft` |
| `ResumeCraft(resume)` | `Resume` model instance | `ResumeCraft` |

### Export Methods

| Method | Returns | Notes |
|---|---|---|
| `rc.to_docx(path)` | `Path` | Creates parent dirs |
| `rc.to_pdf(path)` | `Path` | Requires `resumecraft[pdf]` |
| `rc.to_docx_bytes()` | `bytes` | DOCX as in-memory bytes |
| `rc.to_pdf_bytes()` | `bytes` | Requires `resumecraft[pdf]` |
| `rc.to_dict()` | `dict` | Validated resume as dict |

### Static Methods

| Method | Returns | Notes |
|---|---|---|
| `ResumeCraft.sample()` | `dict` | Complete sample resume |
| `ResumeCraft.json_schema()` | `dict` | Pydantic JSON Schema |
