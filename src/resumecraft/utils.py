import re

from docx.opc.constants import RELATIONSHIP_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph


def keep_with_next(paragraph: Paragraph) -> None:
    """Mark the paragraph so it stays on the same page as the next one."""
    pPr = paragraph._p.get_or_add_pPr()
    pPr.append(OxmlElement("w:keepNext"))


def add_hyperlink(paragraph: Paragraph, text: str, url: str, link_color: str = "0046B4", font_name: str = "Calibri") -> None:
    """Append a clickable hyperlink run to the paragraph."""
    # Get access to the document's relationship part and create a new relation ID
    part = paragraph.part
    r_id = part.relate_to(url, RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    # Create the w:hyperlink tag and link it to the relation ID
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)

    # Create a w:r (run) element for the visible text
    new_run = OxmlElement("w:r")
    # Apply formatting to make it look like a link (blue and underlined)
    rPr = OxmlElement("w:rPr")

    color = OxmlElement("w:color")
    color.set(qn("w:val"), link_color)  # Setting the hyperlink color
    rPr.append(color)

    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")  # Underline
    rPr.append(underline)

    size = OxmlElement("w:sz")
    size.set(qn("w:val"), "19")
    rPr.append(size)

    fonts = OxmlElement("w:rFonts")
    fonts.set(qn("w:ascii"), font_name)
    fonts.set(qn("w:hAnsi"), font_name)
    rPr.append(fonts)

    new_run.append(rPr)

    # Set the text for the run and assemble the elements
    new_run.text = text
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)


def add_bottom_border(paragraph: Paragraph) -> None:
    """Draw a thin black underline below the paragraph (for section headings)."""
    # Access the paragraph's XML element (<w:p>)
    p = paragraph._p
    # Get or create the paragraph properties element (<w:pPr>)
    pPr = p.get_or_add_pPr()
    # Create the paragraph border element (<w:pBdr>)
    pBdr = pPr.makeelement(qn("w:pBdr"), {})
    # Create the bottom border element (<w:bottom>)
    bottom = pBdr.makeelement(
        qn("w:bottom"),
        {
            qn("w:val"): "single",  # Line style (e.g., single, double, dash)
            qn("w:sz"): "4",  # Thickness in 1/8 points (6 = 0.75pt)
            qn("w:space"): "1",  # Padding between text and border
            qn("w:color"): "000000",  # Color (HEX code or 'auto')
        },
    )
    # Append the border to the paragraph border element
    pBdr.append(bottom)
    # Insert the paragraph border element into the properties
    pPr.append(pBdr)


def build_bold_pattern(keywords: list[str]) -> re.Pattern[str] | None:
    """Compile a regex that matches any of the keywords; longer ones first to avoid partial matches."""
    if not keywords:
        return None
    # Get keywords order by length. Longer one comes first
    sorted_kw = sorted(keywords, key=len, reverse=True)
    # Create escaped keywords
    escaped = [re.escape(k) for k in sorted_kw]
    # Return regex
    return re.compile("(" + "|".join(escaped) + ")")
