import json

from resumecraft import ResumeCraft


class TestResumeCraftInit:
    def test_from_dict(self, minimal_resume):
        data = minimal_resume.model_dump()
        rc = ResumeCraft(data)
        assert rc.resume.name == "John Doe"

    def test_from_resume(self, minimal_resume):
        rc = ResumeCraft(minimal_resume)
        assert rc.resume is minimal_resume

    def test_from_json_string(self, minimal_resume):
        json_str = json.dumps(minimal_resume.model_dump())
        rc = ResumeCraft(json_str)
        assert rc.resume.name == "John Doe"

    def test_from_json_file(self, sample_json_path):
        rc = ResumeCraft.from_json(sample_json_path)
        assert rc.resume.name

    def test_repr(self, full_resume):
        rc = ResumeCraft(full_resume)
        assert "ResumeCraft(" in repr(rc)
        assert "Jane Smith" in repr(rc)

    def test_repr_minimal(self, minimal_resume):
        rc = ResumeCraft(minimal_resume)
        assert "sections=1" in repr(rc)  # only summary


class TestSampleAndSchema:
    def test_sample_is_valid(self):
        sample = ResumeCraft.sample()
        rc = ResumeCraft(sample)
        assert rc.resume.name == "Your Name"

    def test_json_schema(self):
        schema = ResumeCraft.json_schema()
        assert schema["type"] == "object"
        assert "name" in schema["properties"]
        assert "contact" in schema["properties"]

    def test_to_dict(self, full_resume):
        rc = ResumeCraft(full_resume)
        data = rc.to_dict()
        assert data["name"] == "Jane Smith"
        assert isinstance(data, dict)

    def test_roundtrip(self, full_resume):
        rc1 = ResumeCraft(full_resume)
        rc2 = ResumeCraft(rc1.to_dict())
        assert rc1.resume.name == rc2.resume.name


class TestToDocx:
    def test_creates_file(self, minimal_resume, tmp_path):
        rc = ResumeCraft(minimal_resume)
        path = rc.to_docx(tmp_path / "out.docx")
        assert path.exists()
        assert path.stat().st_size > 0

    def test_creates_parent_dirs(self, minimal_resume, tmp_path):
        rc = ResumeCraft(minimal_resume)
        path = rc.to_docx(tmp_path / "nested" / "dir" / "out.docx")
        assert path.exists()

    def test_full_resume(self, full_resume, tmp_path):
        rc = ResumeCraft(full_resume)
        path = rc.to_docx(tmp_path / "full.docx")
        assert path.exists()


class TestToBytes:
    def test_returns_bytes(self, minimal_resume):
        rc = ResumeCraft(minimal_resume)
        data = rc.to_bytes()
        assert isinstance(data, bytes)
        assert len(data) > 0

    def test_valid_docx_zip(self, minimal_resume):
        rc = ResumeCraft(minimal_resume)
        data = rc.to_bytes()
        assert data[:2] == b"PK"  # docx is a ZIP archive

    def test_full_resume(self, full_resume):
        rc = ResumeCraft(full_resume)
        data = rc.to_bytes()
        assert len(data) > 0
