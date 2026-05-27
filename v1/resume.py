"""Resume - the main public API."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .models import Contact
from .sections import (
    Award,
    Certification,
    Education,
    Experience,
    Project,
    Section,
    Skill,
    Summary,
)
from .templates import Template, classic
from .widgets.base import BuildContext, Widget
from .widgets.content import Text
from .widgets.document import Document

_TEMPLATES: dict[str, Template] = {
    "classic": classic,
}

_DEFAULT_SECTION_ORDER = [
    "summary",
    "experience",
    "projects",
    "skills",
    "education",
    "certifications",
    "awards",
]

_SECTION_HEADINGS: dict[str, str] = {
    "summary": "Summary",
    "experience": "Experience",
    "projects": "Projects",
    "skills": "Skills",
    "education": "Education",
    "certifications": "Certifications",
    "awards": "Awards",
}


@dataclass
class Resume:
    """Build, load, and export resumes.

    Main API:
        resume = Resume(name="John", contact=Contact(...), children=[...])
        resume = Resume.from_jsonfile("resume.json")
        resume.to_docx("output.docx")
    """

    name: str
    contact: Contact = field(default_factory=Contact)
    photo: str | None = None
    template: Template | str = field(default_factory=lambda: classic)
    bold_keywords: list[str] = field(default_factory=list)
    children: list[Widget] = field(default_factory=list)

    def _resolve_template(self) -> Template:
        if isinstance(self.template, str):
            return _TEMPLATES[self.template]
        return self.template

    def build(self) -> Document:
        """Convert this resume into a Document widget tree."""
        tmpl = self._resolve_template()

        widgets: list[Widget] = []

        widgets.append(_HeaderWidget(
            name=self.name,
            contact=self.contact,
            template=tmpl,
        ))

        for child in self.children:
            widgets.append(child)

        return Document(children=widgets, template=tmpl, bold_words=self.bold_keywords)

    def to_docx(self, path: str) -> None:
        """Build and save as a .docx file."""
        self.build().save(path)

    def to_docx_bytes(self) -> bytes:
        """Build and return raw .docx bytes."""
        return self.build().to_bytes()

    def to_pdf(self, path: str) -> None:
        """Build, save as .docx, convert to PDF. Requires docx2pdf."""
        from docx2pdf import convert

        docx_path = path.replace(".pdf", ".docx")
        self.to_docx(docx_path)
        convert(docx_path, path)
        Path(docx_path).unlink(missing_ok=True)

    def to_pdf_bytes(self) -> bytes:
        """Build and return raw PDF bytes. Requires docx2pdf."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            docx_path = str(Path(tmp) / "resume.docx")
            pdf_path = str(Path(tmp) / "resume.pdf")
            self.to_docx(docx_path)
            from docx2pdf import convert

            convert(docx_path, pdf_path)
            return Path(pdf_path).read_bytes()

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dict (compatible with the JSON format)."""
        data: dict[str, Any] = {"name": self.name}

        contact_dict = self.contact.to_dict()
        if contact_dict:
            data["contact"] = contact_dict

        if self.photo:
            data["photo"] = self.photo

        if self.bold_keywords:
            data["bold_keywords"] = self.bold_keywords

        # Extract sections by type
        section_order: list[str] = []
        for child in self.children:
            if isinstance(child, Section):
                key = _heading_to_key(child.title)
                if key:
                    section_order.append(key)
                    entries = child.children
                    if key == "summary" and entries and isinstance(entries[0], Summary):
                        data["summary"] = entries[0].to_dict()
                    else:
                        data[key] = [e.to_dict() for e in entries if hasattr(e, "to_dict")]

        if section_order and section_order != _DEFAULT_SECTION_ORDER[: len(section_order)]:
            data["section_order"] = section_order

        return data

    def to_json(self, indent: int = 2) -> str:
        """Serialize to a JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def to_yaml(self) -> str:
        """Serialize to a YAML string. Requires pyyaml."""
        import yaml

        return yaml.dump(self.to_dict(), default_flow_style=False, allow_unicode=True, sort_keys=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Resume:
        """Create a Resume from a plain dict."""
        contact = Contact.from_dict(data.get("contact", {}))
        template_name = data.get("style", {}).get("template", "classic")
        template = _TEMPLATES.get(template_name, classic)

        # Apply style overrides
        style = data.get("style", {})
        if font := style.get("font"):
            template = template.copy(font=font)
        if color := style.get("color"):
            template = template.copy(heading_color=color)

        bold_keywords = data.get("bold_keywords", [])
        section_order = data.get("section_order", _DEFAULT_SECTION_ORDER)

        children: list[Widget] = []
        for key in section_order:
            heading = _SECTION_HEADINGS.get(key, key.title())
            if key == "summary" and "summary" in data:
                children.append(Section(heading, [Summary(data["summary"])]))
            elif key == "experience" and "experience" in data:
                children.append(Section(heading, [Experience.from_dict(e) for e in data["experience"]]))
            elif key == "projects" and "projects" in data:
                children.append(Section(heading, [Project.from_dict(p) for p in data["projects"]]))
            elif key == "skills" and "skills" in data:
                children.append(Section(heading, [Skill.from_dict(s) for s in data["skills"]]))
            elif key == "education" and "education" in data:
                children.append(Section(heading, [Education.from_dict(e) for e in data["education"]]))
            elif key == "certifications" and "certifications" in data:
                children.append(Section(heading, [Certification.from_dict(c) for c in data["certifications"]]))
            elif key == "awards" and "awards" in data:
                children.append(Section(heading, [Award.from_dict(a) for a in data["awards"]]))

        return cls(
            name=data["name"],
            contact=contact,
            photo=data.get("photo"),
            template=template,
            bold_keywords=bold_keywords,
            children=children,
        )

    @classmethod
    def from_json(cls, text: str) -> Resume:
        """Create a Resume from a JSON string."""
        return cls.from_dict(json.loads(text))

    @classmethod
    def from_jsonfile(cls, path: str | Path) -> Resume:
        """Create a Resume from a JSON file."""
        return cls.from_json(Path(path).read_text(encoding="utf-8"))

    @classmethod
    def from_yaml(cls, text: str) -> Resume:
        """Create a Resume from a YAML string. Requires pyyaml."""
        import yaml

        return cls.from_dict(yaml.safe_load(text))

    @classmethod
    def from_yamlfile(cls, path: str | Path) -> Resume:
        """Create a Resume from a YAML file. Requires pyyaml."""
        return cls.from_yaml(Path(path).read_text(encoding="utf-8"))

    @classmethod
    def from_bytes(cls, data: bytes) -> Resume:
        """Create a Resume from raw JSON or YAML bytes."""
        text = data.decode("utf-8")
        try:
            return cls.from_json(text)
        except json.JSONDecodeError:
            return cls.from_yaml(text)

    @classmethod
    def json_schema(cls) -> dict[str, Any]:
        """Return a JSON Schema describing the resume data format."""
        # Minimal schema - can be expanded
        return {
            "type": "object",
            "required": ["name", "contact", "summary"],
            "properties": {
                "name": {"type": "string"},
                "photo": {"type": "string"},
                "contact": {"type": "object"},
                "summary": {"type": "string"},
                "bold_keywords": {"type": "array", "items": {"type": "string"}},
                "experience": {"type": "array"},
                "projects": {"type": "array"},
                "skills": {"type": "array"},
                "education": {"type": "array"},
                "certifications": {"type": "array"},
                "awards": {"type": "array"},
                "section_order": {"type": "array", "items": {"type": "string"}},
                "style": {"type": "object"},
            },
        }



@dataclass
class _HeaderWidget(Widget):
    """Renders the resume header (name + contact). Internal."""

    name: str
    contact: Contact
    template: Template

    def build(self, ctx: BuildContext) -> None:
        tmpl = self.template
        Text(self.name, size=tmpl.name_size, bold=True, align="center", space_after=2).build(ctx)
        parts = [p for p in (self.contact.location, self.contact.email, self.contact.phone) if p]
        if parts:
            Text(" | ".join(parts), size=tmpl.contact_size, align="center",
                 space_before=0, space_after=2).build(ctx)
        if self.contact.links:
            Text(" | ".join(link.label for link in self.contact.links),
                 size=tmpl.contact_size, align="center", space_before=0, space_after=2).build(ctx)


def _heading_to_key(heading: str) -> str | None:
    """Convert a section heading back to a dict key."""
    mapping = {v.lower(): k for k, v in _SECTION_HEADINGS.items()}
    return mapping.get(heading.lower())
