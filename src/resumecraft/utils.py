import re

from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph


def keep_with_next(paragraph: Paragraph) -> None:
    pPr = paragraph._p.get_or_add_pPr()
    pPr.append(OxmlElement("w:keepNext"))


def add_hyperlink(paragraph: Paragraph, text: str, url: str, link_color: str = "0046B4", font_name: str = "Calibri") -> None:
    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )

    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)

    new_run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")

    color = OxmlElement("w:color")
    color.set(qn("w:val"), link_color)
    rPr.append(color)

    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    rPr.append(underline)

    size = OxmlElement("w:sz")
    size.set(qn("w:val"), "19")
    rPr.append(size)

    fonts = OxmlElement("w:rFonts")
    fonts.set(qn("w:ascii"), font_name)
    fonts.set(qn("w:hAnsi"), font_name)
    rPr.append(fonts)

    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)


def add_bottom_border(paragraph: Paragraph) -> None:
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = pPr.makeelement(qn("w:pBdr"), {})
    bottom = pBdr.makeelement(
        qn("w:bottom"),
        {
            qn("w:val"): "single",
            qn("w:sz"): "4",
            qn("w:space"): "1",
            qn("w:color"): "000000",
        },
    )
    pBdr.append(bottom)
    pPr.append(pBdr)


def build_bold_pattern(keywords: list[str]) -> re.Pattern | None:
    if not keywords:
        return None
    sorted_kw = sorted(keywords, key=len, reverse=True)
    escaped = [re.escape(k) for k in sorted_kw]
    return re.compile("(" + "|".join(escaped) + ")")
