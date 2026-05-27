import io
from pathlib import Path

from docx import Document
from docx.document import Document as DocumentObject
from docx.shared import Pt

from resumecraft.models import DEFAULT_SECTION_ORDER, Resume
from resumecraft.render import RenderContext
from resumecraft.sections import (
    DEFAULT_HEADINGS,
    SECTION_REGISTRY,
    HeaderSection,
)
from resumecraft.styles import (
    BOTTOM_MARGIN,
    LEFT_MARGIN,
    RIGHT_MARGIN,
    TOP_MARGIN,
    resolve_style,
)
from resumecraft.utils import build_bold_pattern


class DocxBuilder:
    def __init__(self, resume: Resume) -> None:
        self.resume = resume
        self.doc = Document()
        self._style = resolve_style(resume.style)
        self._headings: dict[str, str] = {**DEFAULT_HEADINGS, **resume.headings}  # type: ignore[dict-item]
        self._built = False
        self._setup_document()
        self._ctx = RenderContext(
            doc=self.doc,
            style=self._style,
            bold_pattern=build_bold_pattern(resume.bold_keywords),
            bold_keywords=frozenset(resume.bold_keywords),
            headings=self._headings,
            ats=resume.style.ats,
        )

    def _setup_document(self) -> None:
        for section in self.doc.sections:
            section.top_margin = TOP_MARGIN
            section.bottom_margin = BOTTOM_MARGIN
            section.left_margin = LEFT_MARGIN
            section.right_margin = RIGHT_MARGIN

        style = self.doc.styles["Normal"]
        style.font.name = self._style.font_name
        style.font.size = Pt(10.5)

    def build(self) -> DocumentObject:
        if self._built:
            return self.doc

        HeaderSection().render(self._ctx, self.resume)

        order = self.resume.section_order or DEFAULT_SECTION_ORDER
        for name in order:
            section = SECTION_REGISTRY[name]
            if section.is_empty(self.resume):
                continue
            section.render(self._ctx, self.resume)

        self._built = True
        return self.doc

    def save(self, path: str | Path) -> Path:
        self.build()
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        self.doc.save(str(target))
        return target

    def to_bytes(self) -> bytes:
        self.build()
        buf = io.BytesIO()
        self.doc.save(buf)
        return buf.getvalue()
