"""Resume section widgets - the main API building blocks."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field

from .widgets.base import BuildContext, Widget
from .widgets.content import Bullet, Heading, Text, TwoCol


@dataclass
class Section(Widget):
    """A titled section with heading and child entries."""

    title: str
    children: Sequence[Widget] = field(default_factory=list)

    def build(self, ctx: BuildContext) -> None:
        tmpl = ctx.template
        Heading(
            self.title,
            size=tmpl.heading_size,
            uppercase=tmpl.heading_uppercase,
            border_bottom=tmpl.heading_border,
            bold=tmpl.heading_bold,
            color=tmpl.heading_color,
            space_before=tmpl.heading_space_before,
            space_after=tmpl.heading_space_after,
        ).build(ctx)
        for i, child in enumerate(self.children):
            child.build(ctx.with_entry_position(is_first=(i == 0)))



@dataclass
class Summary(Widget):
    """Plain text summary paragraph."""

    text: str

    def build(self, ctx: BuildContext) -> None:
        tmpl = ctx.template
        Text(self.text, size=tmpl.body_size, space_after=tmpl.heading_space_after).build(ctx)

    def to_dict(self) -> str:
        return self.text


@dataclass
class Experience(Widget):
    """Single job entry."""

    company: str
    title: str
    location: str = ""
    duration: str = ""
    bullets: list[str] = field(default_factory=list)

    def build(self, ctx: BuildContext) -> None:
        tmpl = ctx.template
        gap = tmpl.first_entry_gap if ctx.is_first_entry else tmpl.entry_gap

        if tmpl.company_first:
            TwoCol(left=self.company, right=self.location, size=tmpl.primary_size,
                    left_bold=True, space_before=gap, space_after=tmpl.line_gap).build(ctx)
            TwoCol(left=self.title, right=self.duration, size=tmpl.secondary_size,
                    left_italic=True, space_before=0, space_after=tmpl.line_gap).build(ctx)
        else:
            TwoCol(left=self.title, right=self.duration, size=tmpl.primary_size,
                    left_bold=True, space_before=gap, space_after=tmpl.line_gap).build(ctx)
            TwoCol(left=self.company, right=self.location, size=tmpl.secondary_size,
                    left_italic=True, space_before=0, space_after=tmpl.line_gap).build(ctx)

        for b in self.bullets:
            Bullet(b, size=tmpl.body_size, space_before=tmpl.bullet_gap,
                   space_after=tmpl.bullet_gap).build(ctx)

    def to_dict(self) -> dict[str, object]:
        d: dict[str, object] = {"company": self.company, "title": self.title}
        if self.location:
            d["location"] = self.location
        if self.duration:
            d["duration"] = self.duration
        if self.bullets:
            d["bullets"] = self.bullets
        return d

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Experience:
        return cls(
            company=str(data["company"]),
            title=str(data["title"]),
            location=str(data.get("location", "")),
            duration=str(data.get("duration", "")),
            bullets=list(data.get("bullets", [])),  # type: ignore[call-overload]
        )


@dataclass
class Project(Widget):
    """Single project entry."""

    name: str
    technologies: str = ""
    duration: str = ""
    bullets: list[str] = field(default_factory=list)

    def build(self, ctx: BuildContext) -> None:
        tmpl = ctx.template
        gap = tmpl.first_entry_gap if ctx.is_first_entry else tmpl.entry_gap

        title = self.name
        if self.technologies:
            title += f"    | {self.technologies}"
        TwoCol(left=title, right=self.duration, size=tmpl.primary_size,
                left_bold=True, space_before=gap, space_after=tmpl.line_gap + 1).build(ctx)

        for b in self.bullets:
            Bullet(b, size=tmpl.body_size, space_before=tmpl.bullet_gap,
                   space_after=tmpl.bullet_gap).build(ctx)

    def to_dict(self) -> dict[str, object]:
        d: dict[str, object] = {"name": self.name}
        if self.technologies:
            d["technologies"] = self.technologies
        if self.duration:
            d["duration"] = self.duration
        if self.bullets:
            d["bullets"] = self.bullets
        return d

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Project:
        return cls(
            name=str(data["name"]),
            technologies=str(data.get("technologies", "")),
            duration=str(data.get("duration", "")),
            bullets=list(data.get("bullets", [])),  # type: ignore[call-overload]
        )


@dataclass
class Skill(Widget):
    """Single skill category and items."""

    category: str
    items: str

    def build(self, ctx: BuildContext) -> None:
        tmpl = ctx.template
        TwoCol(left=f"{self.category}:", right=self.items, size=tmpl.body_size,
                left_bold=True, space_before=0, space_after=tmpl.line_gap).build(ctx)

    def to_dict(self) -> dict[str, str]:
        return {"category": self.category, "items": self.items}

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Skill:
        return cls(category=data["category"], items=data["items"])


@dataclass
class Education(Widget):
    """Single education entry."""

    institution: str
    degree: str
    duration: str = ""

    def build(self, ctx: BuildContext) -> None:
        tmpl = ctx.template
        gap = tmpl.first_entry_gap if ctx.is_first_entry else tmpl.entry_gap
        TwoCol(left=self.degree, right=self.duration, size=tmpl.primary_size,
                left_bold=True, space_before=gap, space_after=tmpl.line_gap).build(ctx)
        Text(self.institution, size=tmpl.secondary_size, italic=True,
             space_before=0, space_after=tmpl.line_gap).build(ctx)

    def to_dict(self) -> dict[str, str]:
        d = {"institution": self.institution, "degree": self.degree}
        if self.duration:
            d["duration"] = self.duration
        return d

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Education:
        return cls(
            institution=data["institution"],
            degree=data["degree"],
            duration=data.get("duration", ""),
        )


@dataclass
class Certification(Widget):
    """Single certification entry."""

    name: str
    issuer: str = ""
    date: str = ""

    def build(self, ctx: BuildContext) -> None:
        tmpl = ctx.template
        gap = tmpl.first_entry_gap if ctx.is_first_entry else tmpl.entry_gap
        TwoCol(left=self.name, right=self.date, size=tmpl.primary_size,
                left_bold=True, space_before=gap, space_after=tmpl.line_gap).build(ctx)
        if self.issuer:
            Text(self.issuer, size=tmpl.secondary_size, italic=True,
                 space_before=0, space_after=tmpl.line_gap).build(ctx)

    def to_dict(self) -> dict[str, str]:
        d = {"name": self.name}
        if self.issuer:
            d["issuer"] = self.issuer
        if self.date:
            d["date"] = self.date
        return d

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Certification:
        return cls(name=data["name"], issuer=data.get("issuer", ""), date=data.get("date", ""))


@dataclass
class Award(Widget):
    """Single award entry."""

    title: str
    issuer: str = ""
    date: str = ""

    def build(self, ctx: BuildContext) -> None:
        tmpl = ctx.template
        gap = tmpl.first_entry_gap if ctx.is_first_entry else tmpl.entry_gap
        TwoCol(left=self.title, right=self.date, size=tmpl.primary_size,
                left_bold=True, space_before=gap, space_after=tmpl.line_gap).build(ctx)
        if self.issuer:
            Text(self.issuer, size=tmpl.secondary_size, italic=True,
                 space_before=0, space_after=tmpl.line_gap).build(ctx)

    def to_dict(self) -> dict[str, str]:
        d = {"title": self.title}
        if self.issuer:
            d["issuer"] = self.issuer
        if self.date:
            d["date"] = self.date
        return d

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Award:
        return cls(title=data["title"], issuer=data.get("issuer", ""), date=data.get("date", ""))
