from pathlib import Path

from resumecraft.builder import DocxBuilder


class TestDocxBuilder:
    def test_build_returns_document(self, minimal_resume):
        builder = DocxBuilder(minimal_resume)
        doc = builder.build()
        assert doc is not None
        assert hasattr(doc, "paragraphs")

    def test_save_creates_file(self, minimal_resume, tmp_path):
        output = tmp_path / "resume.docx"
        builder = DocxBuilder(minimal_resume)
        result = builder.save(output)
        assert result == output
        assert output.exists()
        assert output.stat().st_size > 0

    def test_save_creates_parent_dirs(self, minimal_resume, tmp_path):
        output = tmp_path / "nested" / "dir" / "resume.docx"
        builder = DocxBuilder(minimal_resume)
        builder.save(output)
        assert output.exists()

    def test_full_resume_builds(self, full_resume, tmp_path):
        output = tmp_path / "full.docx"
        builder = DocxBuilder(full_resume)
        builder.save(output)
        assert output.exists()
        assert output.stat().st_size > 0

    def test_document_has_content(self, full_resume):
        builder = DocxBuilder(full_resume)
        doc = builder.build()
        text = "\n".join(p.text for p in doc.paragraphs)
        assert "Jane Smith" in text
        assert "WORK EXPERIENCE" in text
        assert "PROFESSIONAL PROJECTS" in text
        assert "PERSONAL & OPEN SOURCE PROJECTS" in text
        assert "SKILLS" in text
        assert "EDUCATION" in text
        assert "LANGUAGES" in text

    def test_minimal_resume_skips_empty_sections(self, minimal_resume):
        builder = DocxBuilder(minimal_resume)
        doc = builder.build()
        text = "\n".join(p.text for p in doc.paragraphs)
        assert "John Doe" in text
        assert "PROFESSIONAL SUMMARY" in text
        assert "WORK EXPERIENCE" not in text
        assert "SKILLS" not in text
        assert "EDUCATION" not in text

    def test_bold_keywords_applied(self, full_resume):
        builder = DocxBuilder(full_resume)
        doc = builder.build()
        bold_runs = []
        for p in doc.paragraphs:
            for run in p.runs:
                if run.bold and run.text.strip():
                    bold_runs.append(run.text.strip())
        # Section headings and keywords should be bold
        assert "FastAPI" in bold_runs
        assert "React" in bold_runs

    def test_page_margins(self, minimal_resume):
        builder = DocxBuilder(minimal_resume)
        builder.build()
        from resumecraft.styles import BOTTOM_MARGIN, LEFT_MARGIN, RIGHT_MARGIN, TOP_MARGIN
        for section in builder.doc.sections:
            assert section.top_margin == TOP_MARGIN
            assert section.bottom_margin == BOTTOM_MARGIN
            assert section.left_margin == LEFT_MARGIN
            assert section.right_margin == RIGHT_MARGIN

    def test_sample_json_builds(self, sample_json_path, tmp_path):
        from resumecraft.models import Resume
        resume = Resume.from_json(str(sample_json_path))
        output = tmp_path / "sample.docx"
        DocxBuilder(resume).save(output)
        assert output.exists()
