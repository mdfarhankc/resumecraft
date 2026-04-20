from typing import Literal

from pydantic import BaseModel, Field

SectionName = Literal[
    "summary",
    "experience",
    "projects",
    "professional_projects",
    "personal_projects",
    "skills",
    "education",
    "certifications",
    "awards",
    "languages",
]

DEFAULT_SECTION_ORDER: tuple[SectionName, ...] = (
    "summary",
    "experience",
    "projects",
    "professional_projects",
    "personal_projects",
    "skills",
    "education",
    "certifications",
    "awards",
    "languages",
)

VALID_SECTIONS = DEFAULT_SECTION_ORDER


FontName = Literal["calibri", "arial", "times", "garamond", "georgia", "helvetica", "cambria"]
ColorTheme = Literal["black", "navy", "forest", "maroon", "slate", "royal"]
SpacingPreset = Literal["compact", "normal", "relaxed"]


class StyleOptions(BaseModel):
    font: FontName = "calibri"
    color: ColorTheme = "black"
    spacing: SpacingPreset = "normal"
    ats: bool = False


class Link(BaseModel):
    label: str
    url: str


class Contact(BaseModel):
    location: str = Field(min_length=1)
    email: str = Field(min_length=1)
    phone: str = Field(min_length=1)
    links: list[Link] = []


class Experience(BaseModel):
    company: str
    location: str
    title: str
    duration: str
    bullets: list[str]


class Project(BaseModel):
    name: str
    subtitle: str
    tech_stack: str | None = None
    link: Link | None = None
    links: list[Link] = []
    bullets: list[str]

    @property
    def all_links(self) -> list[Link]:
        result = list(self.links)
        if self.link and self.link not in result:
            result.insert(0, self.link)
        return result


class Skill(BaseModel):
    category: str
    items: str


class Education(BaseModel):
    institution: str
    degree: str
    duration: str


class Certification(BaseModel):
    name: str
    issuer: str
    date: str
    link: Link | None = None
    links: list[Link] = []

    @property
    def all_links(self) -> list[Link]:
        result = list(self.links)
        if self.link and self.link not in result:
            result.insert(0, self.link)
        return result


class Award(BaseModel):
    title: str
    issuer: str
    date: str
    description: str | None = None


class Resume(BaseModel):
    name: str
    contact: Contact
    summary: str
    bold_keywords: list[str] = []
    experience: list[Experience] = []
    projects: list[Project] = []
    professional_projects: list[Project] = []
    personal_projects: list[Project] = []
    skills: list[Skill] = []
    education: list[Education] = []
    certifications: list[Certification] = []
    awards: list[Award] = []
    languages: str = ""
    section_order: list[SectionName] | None = None
    headings: dict[str, str] = {}
    style: StyleOptions = StyleOptions()

    @classmethod
    def from_json(cls, path: str) -> "Resume":
        import json
        from pathlib import Path

        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(**data)
