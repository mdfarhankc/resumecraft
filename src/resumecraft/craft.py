from __future__ import annotations

import json
import tempfile
import warnings
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from resumecraft.builder import DocxBuilder
from resumecraft.models import Resume
from resumecraft.samples import sample_resume


class ResumeCraft:
    """Main entry point: load resume data and export to docx/pdf/bytes."""

    def __init__(self, resume: Resume | Mapping[str, Any] | str) -> None:
        if isinstance(resume, Resume):
            self.resume = resume
            return

        warnings.warn(
            "Passing a dict or JSON string directly to ResumeCraft() is deprecated "
            "and will be removed in v1.0. "
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
            self.resume.certifications,
            self.resume.awards,
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
        if isinstance(text, Path):
            warnings.warn(
                "ResumeCraft.from_json() with a file path is deprecated "
                "and will be removed in v1.0. "
                "Use ResumeCraft.from_jsonfile(path) instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            return cls.from_jsonfile(text)
        s = text.lstrip()
        if not s.startswith(("{", "[")):
            warnings.warn(
                "ResumeCraft.from_json() with a file path is deprecated "
                "and will be removed in v1.0. "
                "Use ResumeCraft.from_jsonfile(path) instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            return cls.from_jsonfile(text)
        try:
            return cls.from_dict(json.loads(s))
        except json.JSONDecodeError:
            path = Path(text.strip())
            if path.suffix in (".json", ".yaml", ".yml"):
                warnings.warn(
                    "ResumeCraft.from_json() with a file path is deprecated "
                    "and will be removed in v1.0. "
                    "Use ResumeCraft.from_jsonfile(path) instead.",
                    DeprecationWarning,
                    stacklevel=2,
                )
                return cls.from_jsonfile(path)
            raise

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
    def from_dict(cls, data: Mapping[str, Any]) -> ResumeCraft:
        return cls(Resume.model_validate(data))

    @classmethod
    def from_yamlfile(cls, path: str | Path) -> ResumeCraft:
        text = Path(path).read_text(encoding="utf-8-sig")
        return cls.from_yaml(text)

    @classmethod
    def from_yaml(cls, text: str) -> ResumeCraft:
        try:
            import yaml
        except ImportError:
            raise ImportError(
                "YAML input requires pyyaml. Install with: pip install resumecraft[yaml]"
            ) from None
        return cls.from_dict(yaml.safe_load(text))

    # ---- discovery helpers ----

    @staticmethod
    def sample() -> dict[str, Any]:
        return sample_resume()

    @staticmethod
    def json_schema() -> dict[str, Any]:
        return Resume.model_json_schema()

    # ---- exports ----

    def to_dict(self) -> dict[str, Any]:
        return self.resume.model_dump()

    def to_docx(self, path: str | Path) -> Path:
        return DocxBuilder(self.resume).save(path)

    def to_docx_bytes(self) -> bytes:
        return DocxBuilder(self.resume).to_bytes()

    def to_bytes(self) -> bytes:
        warnings.warn(
            "ResumeCraft.to_bytes() is deprecated and will be removed in v1.0. "
            "Use to_docx_bytes() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.to_docx_bytes()

    def to_pdf(self, path: str | Path) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        self._render_pdf(target)
        return target

    def to_pdf_bytes(self) -> bytes:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            pdf_path = Path(tmp.name)
        try:
            self._render_pdf(pdf_path)
            return pdf_path.read_bytes()
        finally:
            pdf_path.unlink(missing_ok=True)

    def _render_pdf(self, path: Path) -> None:
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
            convert(str(docx_path), str(path))
        finally:
            docx_path.unlink(missing_ok=True)
