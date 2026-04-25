from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

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


FontName = Literal["calibri", "arial", "times",
                   "garamond", "georgia", "helvetica", "cambria"]
ColorTheme = Literal["black", "navy", "forest", "maroon", "slate", "royal"]
SpacingPreset = Literal["compact", "normal", "relaxed"]


_strict = ConfigDict(extra="forbid")


class StyleOptions(BaseModel):
    model_config = _strict

    font: FontName = "calibri"
    color: ColorTheme = "black"
    spacing: SpacingPreset = "normal"
    ats: bool = False


class Link(BaseModel):
    model_config = _strict

    label: str
    url: str


class Contact(BaseModel):
    model_config = _strict

    location: str = Field(min_length=1)
    email: str = Field(min_length=1)
    phone: str = Field(min_length=1)
    links: list[Link] = []


class Experience(BaseModel):
    model_config = _strict

    company: str
    location: str
    title: str
    duration: str
    bullets: list[str]


class Project(BaseModel):
    model_config = _strict

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
    model_config = _strict

    category: str
    items: str


class Education(BaseModel):
    model_config = _strict

    institution: str
    degree: str
    duration: str


class Certification(BaseModel):
    model_config = _strict

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
    model_config = _strict

    title: str
    issuer: str
    date: str
    description: str | None = None


class Resume(BaseModel):
    model_config = _strict

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

    @model_validator(mode="before")
    @classmethod
    def _drop_metadata(cls, data: Any) -> Any:
        # Editor/tooling metadata that should not be validated as resume fields
        if isinstance(data, dict):
            metadata_keys = {"$schema", "_version"}
            if metadata_keys.intersection(data):
                data = {k: v for k, v in data.items() if k not in metadata_keys}
        return data

    @field_validator("section_order")
    @classmethod
    def _no_duplicate_sections(cls, v: list[SectionName] | None) -> list[SectionName] | None:
        if v is not None and len(v) != len(set(v)):
            dupes = sorted({s for s in v if v.count(s) > 1})
            raise ValueError(f"duplicate sections in section_order: {dupes}")
        return v
