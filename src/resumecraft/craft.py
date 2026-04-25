from __future__ import annotations

import io
import json
import tempfile
import warnings
from pathlib import Path
from typing import Any

from resumecraft.builder import DocxBuilder
from resumecraft.models import Resume


class ResumeCraft:
    """Main entry point: load resume data and export to docx/pdf/bytes."""

    def __init__(self, resume: Resume | dict[str, Any] | str) -> None:
        if isinstance(resume, Resume):
            self.resume = resume
            return

        warnings.warn(
            "Passing a dict or JSON string directly to ResumeCraft() is deprecated. "
            "Use ResumeCraft.from_dict() or ResumeCraft.from_json() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        if isinstance(resume, str):
            self.resume = Resume.model_validate(json.loads(resume))
        else:
            self.resume = Resume.model_validate(resume)

    def __repr__(self) -> str:
        filled = [
            self.resume.summary,
            self.resume.experience,
            self.resume.projects,
            self.resume.professional_projects,
            self.resume.personal_projects,
            self.resume.skills,
            self.resume.education,
            self.resume.languages,
        ]
        sections = sum(1 for s in filled if s)
        return f"ResumeCraft(name={self.resume.name!r}, sections={sections})"

    # ---- factories ----

    @classmethod
    def from_jsonfile(cls, path: str | Path) -> ResumeCraft:
        text = Path(path).read_text(encoding="utf-8-sig")
        return cls.from_json(text)

    @classmethod
    def from_json(cls, text: str | Path) -> ResumeCraft:
        # Backward compat: old API was from_json(file_path)
        s = str(text).lstrip()
        if not s.startswith(("{", "[")):
            warnings.warn(
                "ResumeCraft.from_json() with a file path is deprecated. "
                "Use ResumeCraft.from_jsonfile(path) instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            return cls.from_jsonfile(str(text))
        return cls.from_dict(json.loads(s))

    @classmethod
    def from_bytes(cls, data: bytes) -> ResumeCraft:
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError as e:
            raise ValueError(
                "Input is not valid UTF-8. Did you pass a binary file?"
            ) from e
        return cls.from_json(text)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ResumeCraft:
        return cls(Resume.model_validate(data))

    # ---- discovery helpers ----

    @staticmethod
    def sample() -> dict[str, Any]:
        return {
            "name": "Your Name",
            "contact": {
                "location": "City, State, Country",
                "email": "your@email.com",
                "phone": "+1-234-567-8900",
                "links": [
                    {"label": "LinkedIn", "url": "https://linkedin.com/in/yourprofile"},
                    {"label": "GitHub", "url": "https://github.com/yourusername"},
                ],
            },
            "summary": "A brief professional summary about yourself.",
            "bold_keywords": ["Python", "React", "FastAPI"],
            "experience": [
                {
                    "company": "Company Name",
                    "location": "City, Country",
                    "title": "Your Title",
                    "duration": "JAN 2023 - PRESENT",
                    "bullets": ["Describe what you did and the impact it had."],
                }
            ],
            "projects": [
                {
                    "name": "Project Name",
                    "subtitle": "| Description",
                    "tech_stack": "Python, FastAPI",
                    "links": [
                        {"label": "GitHub", "url": "https://github.com/you/project"},
                        {"label": "Live Demo", "url": "https://project.example.com"},
                    ],
                    "bullets": ["Describe the project and your contributions."],
                }
            ],
            "skills": [
                {"category": "Backend", "items": "Python (FastAPI, Django), Node.js"},
                {"category": "Frontend", "items": "React, TypeScript"},
            ],
            "education": [
                {
                    "institution": "University Name",
                    "degree": "Bachelor of Science in Computer Science",
                    "duration": "2019 - 2023",
                }
            ],
            "certifications": [
                {
                    "name": "AWS Certified Developer",
                    "issuer": "Amazon Web Services",
                    "date": "2024",
                    "link": {"label": "Verify", "url": "https://aws.amazon.com/verify"},
                }
            ],
            "awards": [
                {
                    "title": "Employee of the Year",
                    "issuer": "Acme Corp",
                    "date": "2024",
                    "description": "Recognized for outstanding contributions.",
                }
            ],
            "languages": "English - Native  |  Spanish - Professional",
            "style": {
                "font": "calibri",
                "color": "black",
                "spacing": "normal",
            },
            "section_order": [
                "summary",
                "experience",
                "projects",
                "skills",
                "education",
                "certifications",
                "awards",
                "languages",
            ],
        }

    @staticmethod
    def json_schema() -> dict[str, Any]:
        return Resume.model_json_schema()

    # ---- exports ----

    def to_dict(self) -> dict[str, Any]:
        return self.resume.model_dump()

    def to_docx(self, path: str | Path) -> Path:
        return DocxBuilder(self.resume).save(path)

    def to_docx_bytes(self) -> bytes:
        doc = DocxBuilder(self.resume).build()
        buf = io.BytesIO()
        doc.save(buf)
        return buf.getvalue()

    def to_bytes(self) -> bytes:
        warnings.warn(
            "ResumeCraft.to_bytes() is deprecated, use to_docx_bytes() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.to_docx_bytes()

    def to_pdf(self, path: str | Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self._render_pdf(path)
        return path

    def to_pdf_bytes(self) -> bytes:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            pdf_path = Path(tmp.name)
        try:
            self._render_pdf(pdf_path)
            return pdf_path.read_bytes()
        finally:
            pdf_path.unlink(missing_ok=True)

    def _render_pdf(self, target: Path) -> None:
        try:
            from docx2pdf import convert
        except ImportError:
            raise ImportError(
                "PDF export requires docx2pdf. Install with: pip install resumecraft[pdf]"
            ) from None

        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
            docx_path = Path(tmp.name)
        try:
            DocxBuilder(self.resume).save(docx_path)
            convert(str(docx_path), str(target))
        finally:
            docx_path.unlink(missing_ok=True)
