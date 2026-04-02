"""Customize fonts, colors, and spacing."""

from resumecraft import ResumeCraft

data = ResumeCraft.sample()
data["name"] = "Jane Smith"

# Try different styles
data["style"] = {
    "font": "garamond",
    "color": "navy",
    "spacing": "compact",
}

rc = ResumeCraft(data)
rc.to_docx("resume_styled.docx")

# Available options:
# font:    calibri, arial, times, garamond, georgia, helvetica, cambria
# color:   black, navy, forest, maroon, slate, royal
# spacing: compact, normal, relaxed
