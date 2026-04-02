from docx.shared import Pt, Inches, RGBColor

# Page layout
TOP_MARGIN = Inches(0.5)
BOTTOM_MARGIN = Inches(0.5)
LEFT_MARGIN = Inches(0.6)
RIGHT_MARGIN = Inches(0.6)
PAGE_WIDTH = Inches(8.5) - LEFT_MARGIN - RIGHT_MARGIN

# ── Font presets ─────────────────────────────────────────

FONT_MAP = {
    "calibri": "Calibri",
    "arial": "Arial",
    "times": "Times New Roman",
    "garamond": "Garamond",
    "georgia": "Georgia",
    "helvetica": "Helvetica",
    "cambria": "Cambria",
}

# ── Color presets ────────────────────────────────────────
# Each theme defines: heading color, tech line color, link color

COLOR_MAP = {
    "black": {
        "heading": RGBColor(0, 0, 0),
        "tech_line": RGBColor(100, 100, 100),
        "link": "0046B4",
    },
    "navy": {
        "heading": RGBColor(0, 32, 96),
        "tech_line": RGBColor(80, 100, 130),
        "link": "002060",
    },
    "forest": {
        "heading": RGBColor(34, 85, 51),
        "tech_line": RGBColor(80, 115, 90),
        "link": "1B5E20",
    },
    "maroon": {
        "heading": RGBColor(128, 0, 0),
        "tech_line": RGBColor(140, 80, 80),
        "link": "800000",
    },
    "slate": {
        "heading": RGBColor(60, 60, 75),
        "tech_line": RGBColor(100, 100, 115),
        "link": "37474F",
    },
    "royal": {
        "heading": RGBColor(63, 13, 124),
        "tech_line": RGBColor(100, 70, 130),
        "link": "4A148C",
    },
}

# ── Spacing presets ──────────────────────────────────────

SPACING_MAP = {
    "compact": {
        "section_space_before": Pt(6),
        "section_space_after": Pt(2),
        "bullet_space": Pt(0),
        "job_space_before": Pt(4),
    },
    "normal": {
        "section_space_before": Pt(8),
        "section_space_after": Pt(4),
        "bullet_space": Pt(1),
        "job_space_before": Pt(6),
    },
    "relaxed": {
        "section_space_before": Pt(10),
        "section_space_after": Pt(6),
        "bullet_space": Pt(2),
        "job_space_before": Pt(8),
    },
}

# ── Font sizes (unchanged across presets) ────────────────

NAME_SIZE = Pt(22)
CONTACT_SIZE = Pt(9.5)
SECTION_HEADING_SIZE = Pt(12)
BODY_SIZE = Pt(10)
COMPANY_SIZE = Pt(10.5)
TECH_LINE_SIZE = Pt(9.5)


def resolve_style(style):
    """Resolve a StyleOptions into concrete style values."""
    font_name = FONT_MAP[style.font]
    colors = COLOR_MAP[style.color]
    spacing = SPACING_MAP[style.spacing]

    return {
        "font_name": font_name,
        "heading_color": colors["heading"],
        "tech_line_color": colors["tech_line"],
        "link_color": colors["link"],
        "section_space_before": spacing["section_space_before"],
        "section_space_after": spacing["section_space_after"],
        "bullet_space": spacing["bullet_space"],
        "job_space_before": spacing["job_space_before"],
    }
