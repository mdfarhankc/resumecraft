"""Template configuration that controls how resume sections render."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any


@dataclass(frozen=True)
class Template:
    """Style configuration for resume rendering. All sizes in points, margins in inches."""

    # Document
    font: str = "Calibri"
    font_size: float = 10
    margin_top: float = 0.5
    margin_bottom: float = 0.5
    margin_left: float = 0.6
    margin_right: float = 0.6

    # Header
    name_size: float = 22
    contact_size: float = 9.5

    # Section headings
    heading_size: float = 12
    heading_uppercase: bool = True
    heading_border: bool = True
    heading_bold: bool = True
    heading_color: str | None = None
    heading_space_before: float = 8
    heading_space_after: float = 4

    # Entry layout
    primary_size: float = 10.5
    secondary_size: float = 10
    body_size: float = 10
    company_first: bool = True

    # Spacing
    entry_gap: float = 8
    first_entry_gap: float = 6
    line_gap: float = 1
    bullet_gap: float = 1

    def copy(self, **overrides: Any) -> Template:
        """Return a new Template with the given fields overridden."""
        return replace(self, **overrides)
