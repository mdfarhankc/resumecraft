"""FastAPI endpoint that returns a generated resume.

Run:
    pip install fastapi uvicorn resumecraft[pdf]
    uvicorn examples.web:app --reload

The same pattern works for Flask and Django -- swap the response object.
"""

import io

from fastapi import FastAPI, UploadFile
from fastapi.responses import Response, StreamingResponse

from resumecraft import ResumeCraft

app = FastAPI()


@app.post("/resume/docx")
def docx(data: dict):
    rc = ResumeCraft.from_dict(data)
    return StreamingResponse(
        io.BytesIO(rc.to_docx_bytes()),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=resume.docx"},
    )


@app.post("/resume/pdf")
def pdf(data: dict):
    return Response(
        ResumeCraft.from_dict(data).to_pdf_bytes(),
        media_type="application/pdf",
    )


@app.post("/resume/upload")
async def upload(file: UploadFile):
    rc = ResumeCraft.from_bytes(await file.read())
    return Response(rc.to_pdf_bytes(), media_type="application/pdf")


@app.get("/resume/sample")
def sample():
    return ResumeCraft.sample()


@app.get("/resume/schema")
def schema():
    return ResumeCraft.json_schema()
