"""FastAPI app that generates resumes via API.

Run:
    pip install fastapi uvicorn resumecraft[pdf]
    uvicorn examples.fastapi_app:app --reload

Test:
    curl -X POST http://localhost:8000/resume/docx \
        -H "Content-Type: application/json" \
        -d @resume.json --output resume.docx
"""

import io
import tempfile

from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from resumecraft import ResumeCraft

app = FastAPI(title="ResumeCraft API")


@app.post("/resume/docx")
def generate_docx(data: dict):
    """Generate a .docx resume."""
    rc = ResumeCraft(data)
    return StreamingResponse(
        io.BytesIO(rc.to_bytes()),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=resume.docx"},
    )


@app.post("/resume/pdf")
def generate_pdf(data: dict):
    """Generate a PDF resume."""
    rc = ResumeCraft(data)
    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    rc.to_pdf(tmp.name)
    return FileResponse(tmp.name, filename="resume.pdf", media_type="application/pdf")


@app.get("/resume/sample")
def get_sample():
    """Return a sample resume JSON to see all available fields."""
    return ResumeCraft.sample()


@app.get("/resume/schema")
def get_schema():
    """Return the JSON schema for resume data."""
    return ResumeCraft.json_schema()
