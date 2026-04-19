from resumecraft import ResumeCraft

data = ResumeCraft.sample()
data["name"] = "Jane Smith"
data["style"] = {
    "font": "garamond",
    "color": "navy",
    "spacing": "compact",
}

rc = ResumeCraft(data)
rc.to_docx("resume_styled.docx")

# font:    calibri, arial, times, garamond, georgia, helvetica, cambria
# color:   black, navy, forest, maroon, slate, royal
# spacing: compact, normal, relaxed
