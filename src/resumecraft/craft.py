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

    def __init__(self, data: dict[str, Any] | Resume) -> None:
        if isinstance(data, Resume):
            self.resume = data
        else:
            self.resume = Resume.model_validate(data)

    @classmethod
    def from_json(cls, path: str | Path) -> ResumeCraft:
        """Load resume data from a JSON file."""
        text = Path(path).read_text(encoding="utf-8")
        return cls(json.loads(text))

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
