"""Classic single-column resume template - clean, traditional, ATS-friendly."""

from __future__ import annotations

from .base import Template

classic = Template(
    font="Calibri",
    font_size=10,
    margin_top=0.5,
    margin_bottom=0.5,
    margin_left=0.6,
    margin_right=0.6,
    name_size=22,
    contact_size=9.5,
    heading_size=12,
    heading_uppercase=True,
    heading_border=True,
    heading_bold=True,
    heading_color=None,
    heading_space_before=8,
    heading_space_after=4,
    primary_size=10.5,
    secondary_size=10,
    body_size=10,
    company_first=True,
    entry_gap=8,
    first_entry_gap=6,
    line_gap=1,
    bullet_gap=1,
)
