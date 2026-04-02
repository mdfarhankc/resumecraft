"""Django view for generating resumes.

Add to your urls.py:
    from examples.django_view import generate_docx, generate_pdf

    urlpatterns = [
        path("resume/docx", generate_docx),
        path("resume/pdf", generate_pdf),
    ]
"""

import json
import tempfile

from django.http import FileResponse, HttpResponse
from resumecraft import ResumeCraft


def generate_docx(request):
    """Generate a .docx resume."""
    data = json.loads(request.body)
    rc = ResumeCraft(data)
    response = HttpResponse(
        rc.to_bytes(),
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    response["Content-Disposition"] = "attachment; filename=resume.docx"
    return response


def generate_pdf(request):
    """Generate a PDF resume."""
    data = json.loads(request.body)
    rc = ResumeCraft(data)
    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    rc.to_pdf(tmp.name)
    return FileResponse(tmp.name, content_type="application/pdf", filename="resume.pdf")
