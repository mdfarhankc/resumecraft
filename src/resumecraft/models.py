from typing import Literal

from pydantic import BaseModel

VALID_SECTIONS = (
    "summary",
    "experience",
    "professional_projects",
    "personal_projects",
    "skills",
    "education",
    "languages",
)

SectionName = Literal[
    "summary",
    "experience",
    "professional_projects",
    "personal_projects",
    "skills",
    "education",
    "languages",
]

DEFAULT_SECTION_ORDER: list[SectionName] = list(VALID_SECTIONS)


class Link(BaseModel):
    label: str
    url: str


class Contact(BaseModel):
    location: str
    email: str
    phone: str
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
    bullets: list[str]


class Skill(BaseModel):
    category: str
    items: str


class Education(BaseModel):
    institution: str
    degree: str
    duration: str


class Resume(BaseModel):
    name: str
    contact: Contact
    summary: str
    bold_keywords: list[str] = []
    experience: list[Experience] = []
    professional_projects: list[Project] = []
    personal_projects: list[Project] = []
    skills: list[Skill] = []
    education: list[Education] = []
    languages: str = ""
    section_order: list[SectionName] | None = None

    @classmethod
    def from_json(cls, path: str) -> "Resume":
        import json
        from pathlib import Path

        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(**data)
