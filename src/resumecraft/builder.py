import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.shared import Pt

from resumecraft.models import DEFAULT_SECTION_ORDER, Education, Experience, Project, Resume, Skill
from resumecraft.styles import (
    BODY_SIZE,
    BOTTOM_MARGIN,
    BULLET_SPACE,
    COMPANY_SIZE,
    CONTACT_SIZE,
    FONT_NAME,
    HEADING_COLOR,
    JOB_SPACE_BEFORE,
    LEFT_MARGIN,
    NAME_SIZE,
    PAGE_WIDTH,
    RIGHT_MARGIN,
    SECTION_HEADING_SIZE,
    SECTION_SPACE_AFTER,
    SECTION_SPACE_BEFORE,
    TECH_LINE_COLOR,
    TECH_LINE_SIZE,
    TOP_MARGIN,
)
from resumecraft.utils import (
    add_bottom_border,
    add_hyperlink,
    build_bold_pattern,
    keep_with_next,
)


class DocxBuilder:
    def __init__(self, resume: Resume) -> None:
        self.resume = resume
        self.doc = Document()
        self._bold_pattern = build_bold_pattern(resume.bold_keywords)
        self._setup_document()

    def _setup_document(self) -> None:
        for section in self.doc.sections:
            section.top_margin = TOP_MARGIN
            section.bottom_margin = BOTTOM_MARGIN
            section.left_margin = LEFT_MARGIN
            section.right_margin = RIGHT_MARGIN

        style = self.doc.styles["Normal"]
        style.font.name = FONT_NAME
        style.font.size = Pt(10.5)

    def _run(self, paragraph, text: str, bold=False, italic=False, size=None, font=None):
        run = paragraph.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.size = size or BODY_SIZE
        run.font.name = font or FONT_NAME
        return run

    # ── Section builders ──────────────────────────────────────

    def _add_section_heading(self, text: str):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = SECTION_SPACE_BEFORE
        p.paragraph_format.space_after = SECTION_SPACE_AFTER
        run = p.add_run(text)
        run.bold = True
        run.font.size = SECTION_HEADING_SIZE
        run.font.name = FONT_NAME
        run.font.color.rgb = HEADING_COLOR
        add_bottom_border(p)
        keep_with_next(p)
        return p

    def _add_two_column_line(
        self, left: str, right: str, left_bold=True, left_italic=False, left_size=None
    ):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.tab_stops.add_tab_stop(PAGE_WIDTH, WD_TAB_ALIGNMENT.RIGHT)

        self._run(p, left, bold=left_bold, italic=left_italic, size=left_size or COMPANY_SIZE)
        p.add_run("\t")
        self._run(p, right, size=BODY_SIZE)

        keep_with_next(p)
        return p

    def _add_rich_bullet(self, text: str):
        p = self.doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = BULLET_SPACE
        p.paragraph_format.space_before = BULLET_SPACE

        if self._bold_pattern:
            parts = self._bold_pattern.split(text)
            keywords_set = set(self.resume.bold_keywords)
            for part in parts:
                if not part:
                    continue
                run = p.add_run(part)
                run.font.size = BODY_SIZE
                run.font.name = FONT_NAME
                if part in keywords_set:
                    run.bold = True
        else:
            self._run(p, text)

        return p

    def _add_project_header(self, name: str, subtitle: str):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = JOB_SPACE_BEFORE
        p.paragraph_format.space_after = Pt(2)
        self._run(p, name, bold=True, size=COMPANY_SIZE)
        self._run(p, f"    {subtitle}", size=BODY_SIZE)
        keep_with_next(p)
        return p

    def _add_tech_line(self, text: str):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(text)
        run.italic = True
        run.font.size = TECH_LINE_SIZE
        run.font.name = FONT_NAME
        run.font.color.rgb = TECH_LINE_COLOR
        keep_with_next(p)

    def _add_link_line(self, label: str, url: str):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        self._run(p, label, size=TECH_LINE_SIZE)
        add_hyperlink(p, url, url)
        keep_with_next(p)

    # ── Top-level section renderers ───────────────────────────

    def _build_header(self) -> None:
        resume = self.resume

        # Name
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(0)
        self._run(p, resume.name, bold=True, size=NAME_SIZE)

        # Contact line
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)

        contact = resume.contact
        self._run(p, f"{contact.location}  |  ", size=CONTACT_SIZE)
        add_hyperlink(p, contact.email, f"mailto:{contact.email}")
        self._run(p, f"  |  {contact.phone}", size=CONTACT_SIZE)

        for link in contact.links:
            self._run(p, "  |  ", size=CONTACT_SIZE)
            add_hyperlink(p, link.label, link.url)

    def _build_summary(self) -> None:
        self._add_section_heading("PROFESSIONAL SUMMARY")
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        self._run(p, self.resume.summary)

    def _build_experience(self) -> None:
        if not self.resume.experience:
            return

        self._add_section_heading("WORK EXPERIENCE")

        for i, exp in enumerate(self.resume.experience):
            p = self._add_two_column_line(exp.company, exp.location)
            p.paragraph_format.space_before = JOB_SPACE_BEFORE if i == 0 else Pt(8)
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
            if proj.link:
                self._add_link_line(f"{proj.link.label}: ", proj.link.url)
            for bullet in proj.bullets:
                self._add_rich_bullet(bullet)

    def _build_skills(self) -> None:
        if not self.resume.skills:
            return

        self._add_section_heading("SKILLS")

        for skill in self.resume.skills:
            p = self.doc.add_paragraph()
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.space_before = Pt(1)
            self._run(p, f"{skill.category}: ", bold=True)
            self._run(p, skill.items)

    def _build_education(self) -> None:
        if not self.resume.education:
            return

        self._add_section_heading("EDUCATION")

        for edu in self.resume.education:
            p = self._add_two_column_line(edu.institution, edu.duration)
            p.paragraph_format.space_before = Pt(2)
            p2 = self.doc.add_paragraph()
            p2.paragraph_format.space_before = Pt(0)
            self._run(p2, edu.degree, italic=True)

    def _build_languages(self) -> None:
        if not self.resume.languages:
            return

        self._add_section_heading("LANGUAGES")
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(1)
        self._run(p, self.resume.languages)

    # ── Public API ────────────────────────────────────────────

    def build(self) -> Document:
        self._build_header()

        section_builders = {
            "summary": self._build_summary,
            "experience": self._build_experience,
            "professional_projects": lambda: self._build_projects(
                self.resume.professional_projects, "PROFESSIONAL PROJECTS"
            ),
            "personal_projects": lambda: self._build_projects(
                self.resume.personal_projects, "PERSONAL & OPEN SOURCE PROJECTS"
            ),
            "skills": self._build_skills,
            "education": self._build_education,
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
