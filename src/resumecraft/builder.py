from pathlib import Path
from typing import Any

from docx import Document
from docx.document import Document as DocumentObject
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.shared import Pt

from resumecraft.models import (
    DEFAULT_SECTION_ORDER,
    Project,
    Resume,
)
from resumecraft.styles import (
    BODY_SIZE,
    BOTTOM_MARGIN,
    COMPANY_SIZE,
    CONTACT_SIZE,
    LEFT_MARGIN,
    NAME_SIZE,
    PAGE_WIDTH,
    RIGHT_MARGIN,
    SECTION_HEADING_SIZE,
    TECH_LINE_SIZE,
    TOP_MARGIN,
    resolve_style,
)
from resumecraft.utils import (
    add_bottom_border,
    add_hyperlink,
    build_bold_pattern,
    keep_with_next,
)

DEFAULT_HEADINGS = {
    "summary": "PROFESSIONAL SUMMARY",
    "experience": "WORK EXPERIENCE",
    "projects": "PROJECTS",
    "professional_projects": "PROFESSIONAL PROJECTS",
    "personal_projects": "PERSONAL & OPEN SOURCE PROJECTS",
    "skills": "SKILLS",
    "education": "EDUCATION",
    "certifications": "CERTIFICATIONS",
    "awards": "AWARDS & ACHIEVEMENTS",
    "languages": "LANGUAGES",
}


class DocxBuilder:
    def __init__(self, resume: Resume) -> None:
        self.resume = resume
        self.doc = Document()
        self._bold_pattern = build_bold_pattern(resume.bold_keywords)
        self._style = resolve_style(resume.style)
        self._headings = {**DEFAULT_HEADINGS, **resume.headings}
        self._setup_document()

    def _heading(self, section: str) -> str:
        return self._headings.get(section, DEFAULT_HEADINGS[section])

    def _setup_document(self) -> None:
        for section in self.doc.sections:
            section.top_margin = TOP_MARGIN
            section.bottom_margin = BOTTOM_MARGIN
            section.left_margin = LEFT_MARGIN
            section.right_margin = RIGHT_MARGIN

        style = self.doc.styles["Normal"]
        style.font.name = self._style["font_name"]
        style.font.size = Pt(10.5)

    def _run(
        self,
        paragraph: Any,
        text: str,
        bold: bool = False,
        italic: bool = False,
        size: Any = None,
        font: str | None = None,
    ) -> Any:
        run = paragraph.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.size = size or BODY_SIZE
        run.font.name = font or self._style["font_name"]
        return run

    def _add_section_heading(self, text: str) -> Any:
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = self._style["section_space_before"]
        p.paragraph_format.space_after = self._style["section_space_after"]
        run = p.add_run(text)
        run.bold = True
        run.font.size = SECTION_HEADING_SIZE
        run.font.name = self._style["font_name"]
        run.font.color.rgb = self._style["heading_color"]
        add_bottom_border(p)
        keep_with_next(p)
        return p

    def _add_two_column_line(
        self,
        left: str,
        right: str,
        left_bold: bool = True,
        left_italic: bool = False,
        left_size: Any = None,
    ) -> Any:
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.tab_stops.add_tab_stop(PAGE_WIDTH, WD_TAB_ALIGNMENT.RIGHT)

        self._run(p, left, bold=left_bold, italic=left_italic, size=left_size or COMPANY_SIZE)
        p.add_run("\t")
        self._run(p, right, size=BODY_SIZE)

        keep_with_next(p)
        return p

    def _add_rich_bullet(self, text: str) -> Any:
        p = self.doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = self._style["bullet_space"]
        p.paragraph_format.space_before = self._style["bullet_space"]

        if self._bold_pattern:
            parts = self._bold_pattern.split(text)
            keywords_set = set(self.resume.bold_keywords)
            for part in parts:
                if not part:
                    continue
                run = p.add_run(part)
                run.font.size = BODY_SIZE
                run.font.name = self._style["font_name"]
                if part in keywords_set:
                    run.bold = True
        else:
            self._run(p, text)

        return p

    def _add_project_header(self, name: str, subtitle: str) -> Any:
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = self._style["job_space_before"]
        p.paragraph_format.space_after = Pt(2)
        self._run(p, name, bold=True, size=COMPANY_SIZE)
        self._run(p, f"    {subtitle}", size=BODY_SIZE)
        keep_with_next(p)
        return p

    def _add_tech_line(self, text: str) -> None:
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(text)
        run.italic = True
        run.font.size = TECH_LINE_SIZE
        run.font.name = self._style["font_name"]
        run.font.color.rgb = self._style["tech_line_color"]
        keep_with_next(p)

    def _add_link_line(self, label: str, url: str) -> None:
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        self._run(p, label, size=TECH_LINE_SIZE)
        add_hyperlink(p, url, url, self._style["link_color"], self._style["font_name"])
        keep_with_next(p)

    def _build_header(self) -> None:
        resume = self.resume

        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(0)
        self._run(p, resume.name, bold=True, size=NAME_SIZE)

        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)

        contact = resume.contact
        self._run(p, f"{contact.location}  |  ", size=CONTACT_SIZE)
        add_hyperlink(p, contact.email, f"mailto:{contact.email}", self._style["link_color"], self._style["font_name"])
        self._run(p, f"  |  {contact.phone}", size=CONTACT_SIZE)

        for link in contact.links:
            self._run(p, "  |  ", size=CONTACT_SIZE)
            add_hyperlink(p, link.label, link.url, self._style["link_color"], self._style["font_name"])

    def _build_summary(self) -> None:
        self._add_section_heading(self._heading("summary"))
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        self._run(p, self.resume.summary)

    def _build_experience(self) -> None:
        if not self.resume.experience:
            return

        self._add_section_heading(self._heading("experience"))

        for i, exp in enumerate(self.resume.experience):
            p = self._add_two_column_line(exp.company, exp.location)
            p.paragraph_format.space_before = self._style["job_space_before"] if i == 0 else Pt(8)
            self._add_two_column_line(
                exp.title, exp.duration, left_bold=False, left_italic=True, left_size=BODY_SIZE
            )
            for bullet in exp.bullets:
                self._add_rich_bullet(bullet)

    def _build_projects(self, projects: list[Project], heading: str) -> None:
        if not projects:
            return

        self._add_section_heading(heading)

        for proj in projects:
            self._add_project_header(proj.name, proj.subtitle)
            if proj.tech_stack:
                self._add_tech_line(proj.tech_stack)
            for link in proj.all_links:
                self._add_link_line(f"{link.label}: ", link.url)
            for bullet in proj.bullets:
                self._add_rich_bullet(bullet)

    def _build_skills(self) -> None:
        if not self.resume.skills:
            return

        self._add_section_heading(self._heading("skills"))

        for skill in self.resume.skills:
            p = self.doc.add_paragraph()
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.space_before = Pt(1)
            self._run(p, f"{skill.category}: ", bold=True)
            self._run(p, skill.items)

    def _build_education(self) -> None:
        if not self.resume.education:
            return

        self._add_section_heading(self._heading("education"))

        for edu in self.resume.education:
            p = self._add_two_column_line(edu.institution, edu.duration)
            p.paragraph_format.space_before = Pt(2)
            p2 = self.doc.add_paragraph()
            p2.paragraph_format.space_before = Pt(0)
            self._run(p2, edu.degree, italic=True)

    def _build_certifications(self) -> None:
        if not self.resume.certifications:
            return

        self._add_section_heading(self._heading("certifications"))

        for cert in self.resume.certifications:
            p = self._add_two_column_line(cert.name, cert.date)
            p.paragraph_format.space_before = Pt(2)
            p2 = self.doc.add_paragraph()
            p2.paragraph_format.space_before = Pt(0)
            self._run(p2, cert.issuer, italic=True)
            for link in cert.all_links:
                self._add_link_line(f"{link.label}: ", link.url)

    def _build_awards(self) -> None:
        if not self.resume.awards:
            return

        self._add_section_heading(self._heading("awards"))

        for award in self.resume.awards:
            p = self._add_two_column_line(award.title, award.date)
            p.paragraph_format.space_before = Pt(2)
            p2 = self.doc.add_paragraph()
            p2.paragraph_format.space_before = Pt(0)
            self._run(p2, award.issuer, italic=True)
            if award.description:
                p3 = self.doc.add_paragraph()
                p3.paragraph_format.space_before = Pt(0)
                self._run(p3, award.description)

    def _build_languages(self) -> None:
        if not self.resume.languages:
            return

        self._add_section_heading(self._heading("languages"))
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(1)
        self._run(p, self.resume.languages)

    def build(self) -> DocumentObject:
        self._build_header()

        section_builders = {
            "summary": self._build_summary,
            "experience": self._build_experience,
            "projects": lambda: self._build_projects(
                self.resume.projects, self._heading("projects")
            ),
            "professional_projects": lambda: self._build_projects(
                self.resume.professional_projects, self._heading("professional_projects")
            ),
            "personal_projects": lambda: self._build_projects(
                self.resume.personal_projects, self._heading("personal_projects")
            ),
            "skills": self._build_skills,
            "education": self._build_education,
            "certifications": self._build_certifications,
            "awards": self._build_awards,
            "languages": self._build_languages,
        }

        order = self.resume.section_order or DEFAULT_SECTION_ORDER
        for section in order:
            section_builders[section]()

        return self.doc

    def save(self, output_path: str | Path) -> Path:
        self.build()
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.doc.save(str(path))
        return path
