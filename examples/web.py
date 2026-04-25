"""FastAPI endpoint that returns a generated resume.

Run:
    pip install fastapi uvicorn resumecraft[pdf]
    uvicorn examples.web:app --reload

The same pattern works for Flask and Django -- swap the response object.
"""

import io
import tempfile

from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse

from resumecraft import ResumeCraft

app = FastAPI()


@app.post("/resume/docx")
def docx(data: dict):
    rc = ResumeCraft(data)
    return StreamingResponse(
        io.BytesIO(rc.to_bytes()),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=resume.docx"},
    )


@app.post("/resume/pdf")
def pdf(data: dict):
    rc = ResumeCraft(data)
    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    rc.to_pdf(tmp.name)
    return FileResponse(tmp.name, filename="resume.pdf", media_type="application/pdf")


@app.get("/resume/sample")
def sample():
    return ResumeCraft.sample()


@app.get("/resume/schema")
def schema():
    return ResumeCraft.json_schema()
