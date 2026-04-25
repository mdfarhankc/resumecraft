"""Sample resume data used by ResumeCraft.sample() and the CLI's init command."""

from typing import Any


def sample_resume() -> dict[str, Any]:
    """Return a fresh sample resume dict with every field populated."""
    return {
        "name": "Your Name",
        "contact": {
            "location": "City, State, Country",
            "email": "your@email.com",
            "phone": "+1-234-567-8900",
            "links": [
                {"label": "LinkedIn", "url": "https://linkedin.com/in/yourprofile"},
                {"label": "GitHub", "url": "https://github.com/yourusername"},
            ],
        },
        "summary": "A brief professional summary about yourself.",
        "bold_keywords": ["Python", "React", "FastAPI"],
        "experience": [
            {
                "company": "Company Name",
                "location": "City, Country",
                "title": "Your Title",
                "duration": "JAN 2023 - PRESENT",
                "bullets": ["Describe what you did and the impact it had."],
            }
        ],
        "projects": [
            {
                "name": "Project Name",
                "subtitle": "| Description",
                "tech_stack": "Python, FastAPI",
                "links": [
                    {"label": "GitHub", "url": "https://github.com/you/project"},
                    {"label": "Live Demo", "url": "https://project.example.com"},
                ],
                "bullets": ["Describe the project and your contributions."],
            }
        ],
        "skills": [
            {"category": "Backend", "items": "Python (FastAPI, Django), Node.js"},
            {"category": "Frontend", "items": "React, TypeScript"},
        ],
        "education": [
            {
                "institution": "University Name",
                "degree": "Bachelor of Science in Computer Science",
                "duration": "2019 - 2023",
            }
        ],
        "certifications": [
            {
                "name": "AWS Certified Developer",
                "issuer": "Amazon Web Services",
                "date": "2024",
                "link": {"label": "Verify", "url": "https://aws.amazon.com/verify"},
            }
        ],
        "awards": [
            {
                "title": "Employee of the Year",
                "issuer": "Acme Corp",
                "date": "2024",
                "description": "Recognized for outstanding contributions.",
            }
        ],
        "languages": "English - Native  |  Spanish - Professional",
        "style": {
            "font": "calibri",
            "color": "black",
            "spacing": "normal",
        },
        "section_order": [
            "summary",
            "experience",
            "projects",
            "skills",
            "education",
            "certifications",
            "awards",
            "languages",
        ],
    }
