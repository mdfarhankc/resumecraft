from resumecraft import ResumeCraft

rc = ResumeCraft.from_json("resume.json")
rc.to_docx("resume.docx")
# rc.to_pdf("resume.pdf")  # needs: pip install resumecraft[pdf]

print(f"Built resume for {rc.resume.name}")
