"""High-level facade for building resumes."""

from __future__ import annotations

import io
import json
from pathlib import Path
from typing import Any

from resumecraft.builder import DocxBuilder
from resumecraft.models import Resume


class ResumeCraft:
    """One-stop API for loading resume data and exporting documents.

    Usage::

        from resumecraft import ResumeCraft

        # From a dict
        rc = ResumeCraft({"name": "John", ...})
        rc.to_docx("resume.docx")

        # From a JSON file
        rc = ResumeCraft.from_json("resume.json")
        content = rc.to_bytes()  # for web frameworks
    """

    def __init__(self, data: dict[str, Any] | Resume | str) -> None:
        if isinstance(data, Resume):
            self.resume = data
        elif isinstance(data, str):
            self.resume = Resume.model_validate(json.loads(data))
        else:
            self.resume = Resume.model_validate(data)

    def __repr__(self) -> str:
        sections = sum(1 for s in [
            self.resume.summary,
            self.resume.experience,
            self.resume.projects,
            self.resume.professional_projects,
            self.resume.personal_projects,
            self.resume.skills,
            self.resume.education,
            self.resume.languages,
        ] if s)
        return f"ResumeCraft(name={self.resume.name!r}, sections={sections})"

    @classmethod
    def from_json(cls, path: str | Path) -> ResumeCraft:
        """Load resume data from a JSON file."""
        text = Path(path).read_text(encoding="utf-8")
        return cls(json.loads(text))

    @staticmethod
    def sample() -> dict[str, Any]:
        """Return a sample resume dict showing all available fields."""
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
                    "link": {"label": "GitHub", "url": "https://github.com/you/project"},
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
                "languages",
            ],
        }

    @staticmethod
    def json_schema() -> dict[str, Any]:
        """Return the JSON schema for resume data."""
        return Resume.model_json_schema()

    def to_dict(self) -> dict[str, Any]:
        """Export resume data as a dict."""
        return self.resume.model_dump()

    def to_docx(self, path: str | Path) -> Path:
        """Build and save a .docx file. Returns the output Path."""
        builder = DocxBuilder(self.resume)
        return builder.save(path)

    def to_bytes(self) -> bytes:
        """Build the .docx in memory and return raw bytes.

        Useful for web frameworks (FastAPI, Flask, Django) where you
        want to stream the file without writing to disk.
        """
        builder = DocxBuilder(self.resume)
        doc = builder.build()
        buf = io.BytesIO()
        doc.save(buf)
        return buf.getvalue()
