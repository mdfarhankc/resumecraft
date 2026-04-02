"""Basic usage of ResumeCraft."""

from resumecraft import ResumeCraft

# Start from a sample template
data = ResumeCraft.sample()

# Customize it
data["name"] = "John Doe"
data["contact"]["email"] = "john@example.com"
data["summary"] = "Full-stack developer with 5 years of experience."

# Build
rc = ResumeCraft(data)
rc.to_docx("resume.docx")
print(f"Created resume for {rc.resume.name}")
