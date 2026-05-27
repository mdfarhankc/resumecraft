# Web Framework Integration

ResumeCraft's factory methods and byte exports are designed for web APIs. Load from dicts, bytes, or uploaded files, and return streaming responses.

---

## FastAPI

```python
import io

from fastapi import FastAPI, UploadFile
from fastapi.responses import Response, StreamingResponse

from resumecraft import ResumeCraft

app = FastAPI()


@app.post("/resume/docx")
def generate_docx(data: dict):
    """Accept resume JSON, return a .docx file."""
    rc = ResumeCraft.from_dict(data)
    return StreamingResponse(
        io.BytesIO(rc.to_docx_bytes()),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=resume.docx"},
    )


@app.post("/resume/pdf")
def generate_pdf(data: dict):
    """Accept resume JSON, return a PDF."""
    return Response(
        ResumeCraft.from_dict(data).to_pdf_bytes(),
        media_type="application/pdf",
    )


@app.post("/resume/upload")
async def from_upload(file: UploadFile):
    """Accept an uploaded JSON/YAML file, return a PDF."""
    rc = ResumeCraft.from_bytes(await file.read())
    return Response(rc.to_pdf_bytes(), media_type="application/pdf")


@app.get("/resume/sample")
def sample():
    """Return a sample resume template."""
    return ResumeCraft.sample()


@app.get("/resume/schema")
def schema():
    """Return the JSON Schema for resume validation."""
    return ResumeCraft.json_schema()
```

### Error Handling

Wrap `from_dict()` calls to return proper HTTP errors:

```python
from fastapi import HTTPException
from pydantic import ValidationError


@app.post("/resume/docx")
def generate_docx(data: dict):
    try:
        rc = ResumeCraft.from_dict(data)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    return StreamingResponse(
        io.BytesIO(rc.to_docx_bytes()),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=resume.docx"},
    )
```

---

## Flask

```python
import io

from flask import Flask, request, send_file

from resumecraft import ResumeCraft

app = Flask(__name__)


@app.post("/resume/docx")
def generate_docx():
    """Accept resume JSON, return a .docx file."""
    rc = ResumeCraft.from_dict(request.json)
    return send_file(
        io.BytesIO(rc.to_docx_bytes()),
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        download_name="resume.docx",
    )


@app.post("/resume/pdf")
def generate_pdf():
    """Accept resume JSON, return a PDF."""
    pdf = ResumeCraft.from_dict(request.json).to_pdf_bytes()
    return send_file(
        io.BytesIO(pdf),
        mimetype="application/pdf",
        download_name="resume.pdf",
    )


@app.post("/resume/upload")
def from_upload():
    """Accept an uploaded JSON/YAML file, return a PDF."""
    rc = ResumeCraft.from_bytes(request.files["file"].read())
    return send_file(
        io.BytesIO(rc.to_pdf_bytes()),
        mimetype="application/pdf",
        download_name="resume.pdf",
    )
```

---

## Django

```python
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from resumecraft import ResumeCraft


@csrf_exempt
@require_POST
def generate_docx(request):
    """Accept resume JSON, return a .docx file."""
    data = json.loads(request.body)
    rc = ResumeCraft.from_dict(data)
    response = HttpResponse(
        rc.to_docx_bytes(),
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    response["Content-Disposition"] = "attachment; filename=resume.docx"
    return response


@csrf_exempt
@require_POST
def generate_pdf(request):
    """Accept resume JSON, return a PDF."""
    data = json.loads(request.body)
    rc = ResumeCraft.from_dict(data)
    response = HttpResponse(rc.to_pdf_bytes(), content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=resume.pdf"
    return response


@csrf_exempt
@require_POST
def from_upload(request):
    """Accept an uploaded JSON/YAML file, return a PDF."""
    uploaded = request.FILES["file"]
    rc = ResumeCraft.from_bytes(uploaded.read())
    response = HttpResponse(rc.to_pdf_bytes(), content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=resume.pdf"
    return response
```

Add to your `urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("resume/docx", views.generate_docx),
    path("resume/pdf", views.generate_pdf),
    path("resume/upload", views.from_upload),
]
```
