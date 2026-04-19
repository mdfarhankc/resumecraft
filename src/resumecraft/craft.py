from __future__ import annotations

import io
import json
from pathlib import Path
from typing import Any

from resumecraft.builder import DocxBuilder
from resumecraft.models import Resume


class ResumeCraft:
    """Simple API for loading resume data and exporting to docx/pdf."""

    def __init__(self, data: dict[str, Any] | Resume | str) -> None:
        if isinstance(data, Resume):
            self.resume = data
        elif isinstance(data, str):
            self.resume = Resume.model_validate(json.loads(data))
        else:
            self.resume = Resume.model_validate(data)

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

    @classmethod
    def from_json(cls, path: str | Path) -> ResumeCraft:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(data)

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

    def to_dict(self) -> dict[str, Any]:
        return self.resume.model_dump()

    def to_docx(self, path: str | Path) -> Path:
        return DocxBuilder(self.resume).save(path)

    def to_pdf(self, path: str | Path) -> Path:
        try:
            from docx2pdf import convert
        except ImportError:
            raise ImportError(
                "PDF export requires docx2pdf. Install with: pip install resumecraft[pdf]"
            ) from None

        import tempfile

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
            tmp_path = Path(tmp.name)

        try:
            self.to_docx(tmp_path)
            convert(str(tmp_path), str(path))
        finally:
            tmp_path.unlink(missing_ok=True)

        return path

    def to_bytes(self) -> bytes:
        doc = DocxBuilder(self.resume).build()
        buf = io.BytesIO()
        doc.save(buf)
        return buf.getvalue()
