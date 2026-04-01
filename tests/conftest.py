import pytest

from resumecraft.models import Contact, Education, Experience, Link, Project, Resume, Skill


@pytest.fixture
def minimal_resume():
    """Resume with only required fields."""
    return Resume(
        name="John Doe",
        contact=Contact(
            location="New York, NY",
            email="john@example.com",
            phone="+1-234-567-8900",
        ),
        summary="A software engineer.",
    )


@pytest.fixture
def full_resume():
    """Resume with all fields populated."""
    return Resume(
        name="Jane Smith",
        contact=Contact(
            location="San Francisco, CA",
            email="jane@example.com",
            phone="+1-987-654-3210",
            links=[
                Link(label="LinkedIn", url="https://linkedin.com/in/janesmith"),
                Link(label="GitHub", url="https://github.com/janesmith"),
            ],
        ),
        summary="Full-stack developer with 5 years of experience.",
        bold_keywords=["Python", "FastAPI", "React"],
        experience=[
            Experience(
                company="Acme Corp",
                location="New York, NY",
                title="Senior Developer",
                duration="JAN 2022 - PRESENT",
                bullets=[
                    "Built APIs using FastAPI and PostgreSQL.",
                    "Led a team of 3 developers on the React frontend.",
                ],
            ),
            Experience(
                company="StartUp Inc",
                location="Remote",
                title="Junior Developer",
                duration="JUN 2020 - DEC 2021",
                bullets=["Developed Python microservices."],
            ),
        ],
        professional_projects=[
            Project(
                name="Dashboard Platform",
                subtitle="| Acme Corp | Internal",
                tech_stack="FastAPI, React, PostgreSQL",
                link=None,
                bullets=["Built an analytics dashboard."],
            ),
        ],
        personal_projects=[
            Project(
                name="Open Source CLI",
                subtitle="| Personal Project",
                tech_stack="Python, Click",
                link=Link(label="GitHub", url="https://github.com/janesmith/cli"),
                bullets=["Created a CLI tool for data processing."],
            ),
        ],
        skills=[
            Skill(category="Backend", items="Python (FastAPI, Django), Node.js"),
            Skill(category="Frontend", items="React, TypeScript"),
        ],
        education=[
            Education(
                institution="MIT",
                degree="B.S. Computer Science",
                duration="2016 - 2020",
            ),
        ],
        languages="English - Native  |  Spanish - Professional",
    )


@pytest.fixture
def sample_json_path():
    """Path to the sample JSON template."""
    from pathlib import Path

    return Path(__file__).parent / "fixtures" / "sample.json"
