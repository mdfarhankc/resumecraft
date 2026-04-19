from resumecraft import ResumeCraft

data = ResumeCraft.sample()
data["name"] = "John Doe"
data["contact"]["email"] = "john@example.com"
data["summary"] = "Full-stack developer with 5 years of experience."

rc = ResumeCraft(data)
rc.to_docx("resume.docx")
print(f"Created resume for {rc.resume.name}")
