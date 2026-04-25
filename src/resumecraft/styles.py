from dataclasses import dataclass
from typing import TYPE_CHECKING, NamedTuple

from docx.shared import Inches, Length, Pt, RGBColor

if TYPE_CHECKING:
    from resumecraft.models import StyleOptions


class Palette(NamedTuple):
    heading: RGBColor
    tech_line: RGBColor
    link: str


class Spacing(NamedTuple):
    section_before: Length
    section_after: Length
    bullet: Length
    job_before: Length


@dataclass(frozen=True)
class ResolvedStyle:
    font_name: str
    heading_color: RGBColor
    tech_line_color: RGBColor
    link_color: str
    section_space_before: Length
    section_space_after: Length
    bullet_space: Length
    job_space_before: Length

TOP_MARGIN = Inches(0.5)
BOTTOM_MARGIN = Inches(0.5)
LEFT_MARGIN = Inches(0.6)
RIGHT_MARGIN = Inches(0.6)
PAGE_WIDTH = Inches(8.5) - LEFT_MARGIN - RIGHT_MARGIN

NAME_SIZE = Pt(22)
CONTACT_SIZE = Pt(9.5)
SECTION_HEADING_SIZE = Pt(12)
BODY_SIZE = Pt(10)
COMPANY_SIZE = Pt(10.5)
TECH_LINE_SIZE = Pt(9.5)

FONT_MAP = {
    "calibri": "Calibri",
    "arial": "Arial",
    "times": "Times New Roman",
    "garamond": "Garamond",
    "georgia": "Georgia",
    "helvetica": "Helvetica",
    "cambria": "Cambria",
}

COLOR_MAP: dict[str, Palette] = {
    "black":  Palette(RGBColor(0, 0, 0),     RGBColor(100, 100, 100), "0046B4"),
    "navy":   Palette(RGBColor(0, 32, 96),   RGBColor(80, 100, 130),  "002060"),
    "forest": Palette(RGBColor(34, 85, 51),  RGBColor(80, 115, 90),   "1B5E20"),
    "maroon": Palette(RGBColor(128, 0, 0),   RGBColor(140, 80, 80),   "800000"),
    "slate":  Palette(RGBColor(60, 60, 75),  RGBColor(100, 100, 115), "37474F"),
    "royal":  Palette(RGBColor(63, 13, 124), RGBColor(100, 70, 130),  "4A148C"),
}

SPACING_MAP: dict[str, Spacing] = {
    "compact": Spacing(section_before=Pt(6),  section_after=Pt(2), bullet=Pt(0), job_before=Pt(4)),
    "normal":  Spacing(section_before=Pt(8),  section_after=Pt(4), bullet=Pt(1), job_before=Pt(6)),
    "relaxed": Spacing(section_before=Pt(10), section_after=Pt(6), bullet=Pt(2), job_before=Pt(8)),
}


def resolve_style(style: "StyleOptions") -> ResolvedStyle:
    palette = COLOR_MAP[style.color]
    spacing = SPACING_MAP[style.spacing]
    return ResolvedStyle(
        font_name=FONT_MAP[style.font],
        heading_color=palette.heading,
        tech_line_color=palette.tech_line,
        link_color=palette.link,
        section_space_before=spacing.section_before,
        section_space_after=spacing.section_after,
        bullet_space=spacing.bullet,
        job_space_before=spacing.job_before,
    )
