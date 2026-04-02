"""Build a resume from an existing JSON file."""

from resumecraft import ResumeCraft

rc = ResumeCraft.from_json("resume.json")

# Export as docx
rc.to_docx("resume.docx")

# Export as PDF (requires: pip install resumecraft[pdf])
# rc.to_pdf("resume.pdf")

print(f"Built resume for {rc.resume.name}")
