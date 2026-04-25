"""Building resumes from Python."""

from resumecraft import ResumeCraft

# Load from a JSON file
rc = ResumeCraft.from_json("sample_resume.json")
rc.to_docx("out.docx")

# Or build from a dict and tweak the style
data = ResumeCraft.sample()
data["name"] = "Jane Doe"
data["style"] = {"font": "garamond", "color": "navy", "spacing": "compact"}
ResumeCraft(data).to_docx("styled.docx")

# PDF output (needs: pip install resumecraft[pdf])
# rc.to_pdf("out.pdf")
