import json

import pytest
from pydantic import ValidationError

from resumecraft.models import Contact, Experience, Link, Project, Resume, DEFAULT_SECTION_ORDER


class TestResume:
    def test_minimal_resume(self, minimal_resume):
        assert minimal_resume.name == "John Doe"
        assert minimal_resume.contact.email == "john@example.com"
        assert minimal_resume.bold_keywords == []
        assert minimal_resume.experience == []
        assert minimal_resume.skills == []

    def test_full_resume(self, full_resume):
        assert full_resume.name == "Jane Smith"
        assert len(full_resume.contact.links) == 2
        assert len(full_resume.experience) == 2
        assert len(full_resume.professional_projects) == 1
        assert len(full_resume.personal_projects) == 1
        assert len(full_resume.skills) == 2
        assert len(full_resume.education) == 1
        assert full_resume.languages == "English - Native  |  Spanish - Professional"

    def test_section_order_default_is_none(self, minimal_resume):
        assert minimal_resume.section_order is None

    def test_custom_section_order(self, minimal_resume):
        minimal_resume.section_order = ["skills", "summary", "experience"]
        assert minimal_resume.section_order == ["skills", "summary", "experience"]

    def test_invalid_section_order(self):
        with pytest.raises(ValidationError):
            Resume(
                name="Test",
                contact=Contact(location="NY", email="a@b.com", phone="123"),
                summary="Test",
                section_order=["invalid_section"],
            )

    def test_missing_required_fields(self):
        with pytest.raises(ValidationError) as exc_info:
            Resume(name="Test")
        errors = exc_info.value.errors()
        fields = {e["loc"][0] for e in errors}
        assert "contact" in fields
        assert "summary" in fields

    def test_missing_name(self):
        with pytest.raises(ValidationError):
            Resume(
                contact=Contact(
                    location="NY", email="a@b.com", phone="123"
                ),
                summary="Test",
            )

    def test_from_json(self, sample_json_path, tmp_path):
        resume = Resume.from_json(str(sample_json_path))
        assert resume.name == "JOHN DOE"
        assert resume.contact.email == "johndoe@email.com"

    def test_from_json_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            Resume.from_json("nonexistent.json")

    def test_from_json_invalid(self, tmp_path):
        bad_file = tmp_path / "bad.json"
        bad_file.write_text('{"name": 123}', encoding="utf-8")
        with pytest.raises(ValidationError):
            Resume.from_json(str(bad_file))


class TestContact:
    def test_contact_with_links(self):
        contact = Contact(
            location="NYC",
            email="a@b.com",
            phone="123",
            links=[Link(label="GitHub", url="https://github.com")],
        )
        assert len(contact.links) == 1

    def test_contact_without_links(self):
        contact = Contact(location="NYC", email="a@b.com", phone="123")
        assert contact.links == []


class TestExperience:
    def test_valid_experience(self):
        exp = Experience(
            company="Acme",
            location="NYC",
            title="Dev",
            duration="2023",
            bullets=["Did things."],
        )
        assert exp.company == "Acme"

    def test_missing_bullets(self):
        with pytest.raises(ValidationError):
            Experience(
                company="Acme", location="NYC", title="Dev", duration="2023"
            )


class TestProject:
    def test_project_with_link(self):
        proj = Project(
            name="Test",
            subtitle="| Personal",
            link=Link(label="GitHub", url="https://github.com"),
            bullets=["Built it."],
        )
        assert proj.link.label == "GitHub"
        assert proj.tech_stack is None

    def test_project_with_tech_stack(self):
        proj = Project(
            name="Test",
            subtitle="| Work",
            tech_stack="Python, React",
            bullets=["Built it."],
        )
        assert proj.tech_stack == "Python, React"
        assert proj.link is None
