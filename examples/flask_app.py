"""Flask app that generates resumes via API.

Run:
    pip install flask resumecraft[pdf]
    flask --app examples.flask_app run

Test:
    curl -X POST http://localhost:5000/resume/docx \
        -H "Content-Type: application/json" \
        -d @resume.json --output resume.docx
"""

import io
import tempfile

from flask import Flask, jsonify, request, send_file
from resumecraft import ResumeCraft

app = Flask(__name__)


@app.post("/resume/docx")
def generate_docx():
    """Generate a .docx resume."""
    rc = ResumeCraft(request.json)
    return send_file(
        io.BytesIO(rc.to_bytes()),
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        download_name="resume.docx",
    )


@app.post("/resume/pdf")
def generate_pdf():
    """Generate a PDF resume."""
    rc = ResumeCraft(request.json)
    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    rc.to_pdf(tmp.name)
    return send_file(tmp.name, mimetype="application/pdf", download_name="resume.pdf")


@app.get("/resume/sample")
def get_sample():
    """Return a sample resume JSON to see all available fields."""
    return jsonify(ResumeCraft.sample())


@app.get("/resume/schema")
def get_schema():
    """Return the JSON schema for resume data."""
    return jsonify(ResumeCraft.json_schema())
