"""Data models for resume header information."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Link:
    """A labeled hyperlink (e.g. LinkedIn, GitHub)."""

    label: str
    url: str

    def to_dict(self) -> dict[str, str]:
        return {"label": self.label, "url": self.url}

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Link:
        return cls(label=data["label"], url=data["url"])


@dataclass
class Contact:
    """Resume contact information."""

    location: str = ""
    email: str = ""
    phone: str = ""
    links: list[Link] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        d: dict[str, object] = {}
        if self.location:
            d["location"] = self.location
        if self.email:
            d["email"] = self.email
        if self.phone:
            d["phone"] = self.phone
        if self.links:
            d["links"] = [link.to_dict() for link in self.links]
        return d

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Contact:
        raw_links: list[dict[str, str]] = data.get("links", [])  # type: ignore[assignment]
        links = [Link.from_dict(item) for item in raw_links]
        return cls(
            location=str(data.get("location", "")),
            email=str(data.get("email", "")),
            phone=str(data.get("phone", "")),
            links=links,
        )
