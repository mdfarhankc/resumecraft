"""Low-level docx XML helpers. Internal use only."""

from __future__ import annotations

import io
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import TYPE_CHECKING

from docx.opc.constants import RELATIONSHIP_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

if TYPE_CHECKING:
    from docx.table import Table
    from docx.text.paragraph import Paragraph


def remove_table_borders(table: Table) -> None:
    """Set all borders on a table to 'none' so it renders invisible."""
    tbl_pr = table._tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "none")
        el.set(qn("w:sz"), "0")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "auto")
        borders.append(el)
    tbl_pr.append(borders)


def zero_table_cell_margins(table: Table) -> None:
    """Set all cell margins to zero so table content is flush."""
    tbl_pr = table._tblPr
    margins = OxmlElement("w:tblCellMar")
    for side in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:w"), "0")
        el.set(qn("w:type"), "dxa")
        margins.append(el)
    tbl_pr.append(margins)


def add_bottom_border(paragraph: Paragraph, color: str = "000000") -> None:
    """Draw a thin horizontal line below the paragraph via XML."""
    p_pr = paragraph._p.get_or_add_pPr()
    p_bdr = p_pr.makeelement(qn("w:pBdr"), {})
    bottom = p_bdr.makeelement(
        qn("w:bottom"),
        {
            qn("w:val"): "single",
            qn("w:sz"): "4",
            qn("w:space"): "1",
            qn("w:color"): color.lstrip("#"),
        },
    )
    p_bdr.append(bottom)
    p_pr.append(p_bdr)


def add_hyperlink(
    paragraph: Paragraph,
    text: str,
    url: str,
    font_name: str = "Calibri",
    font_size: float = 11,
    link_color: str = "0563C1",
) -> None:
    """Append a clickable hyperlink run. Built via raw XML because python-docx has no hyperlink API."""
    part = paragraph.part
    r_id = part.relate_to(url, RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)

    run = OxmlElement("w:r")
    r_pr = OxmlElement("w:rPr")

    fonts = OxmlElement("w:rFonts")
    fonts.set(qn("w:ascii"), font_name)
    fonts.set(qn("w:hAnsi"), font_name)
    r_pr.append(fonts)

    sz_val = str(round(font_size * 2))  # docx uses half-points
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), sz_val)
    r_pr.append(sz)
    sz_cs = OxmlElement("w:szCs")
    sz_cs.set(qn("w:val"), sz_val)
    r_pr.append(sz_cs)

    color = OxmlElement("w:color")
    color.set(qn("w:val"), link_color.lstrip("#"))
    r_pr.append(color)

    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    r_pr.append(underline)

    run.append(r_pr)
    run.text = text
    hyperlink.append(run)
    paragraph._p.append(hyperlink)


def clean_empty_first_paragraph(cell: object) -> None:
    """Remove the default empty paragraph from a table cell if content was added."""
    paragraphs = cell.paragraphs  # type: ignore[attr-defined]
    if len(paragraphs) > 1 and not paragraphs[0].text and not paragraphs[0].runs:
        paragraphs[0]._element.getparent().remove(paragraphs[0]._element)


def load_image(source: str) -> io.BytesIO:
    """Load an image from a local path or URL into a BytesIO stream."""
    if source.startswith(("http://", "https://")):
        try:
            with urllib.request.urlopen(source, timeout=30) as resp:
                data = resp.read()
        except urllib.error.HTTPError as e:
            raise ValueError(f"Failed to fetch image: {source} (HTTP {e.code})") from e
        except urllib.error.URLError as e:
            raise ValueError(f"Failed to fetch image: {source} ({e.reason})") from e
    else:
        path = Path(source)
        if not path.is_file():
            raise ValueError(f"Image not found: {source}")
        data = path.read_bytes()

    if not data:
        raise ValueError(f"Image is empty: {source}")

    return io.BytesIO(data)


def build_bold_pattern(keywords: list[str]) -> re.Pattern[str] | None:
    """Compile a regex that matches any keyword. Longer keywords first to avoid partial matches."""
    if not keywords:
        return None
    sorted_kw = sorted(keywords, key=len, reverse=True)
    escaped = [re.escape(k) for k in sorted_kw]
    return re.compile("(" + "|".join(escaped) + ")")
