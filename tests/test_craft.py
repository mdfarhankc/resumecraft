from resumecraft import ResumeCraft


class TestResumeCraftInit:
    def test_from_dict(self, minimal_resume):
        data = minimal_resume.model_dump()
        rc = ResumeCraft(data)
        assert rc.resume.name == "John Doe"

    def test_from_resume(self, minimal_resume):
        rc = ResumeCraft(minimal_resume)
        assert rc.resume is minimal_resume

    def test_from_json(self, sample_json_path):
        rc = ResumeCraft.from_json(sample_json_path)
        assert rc.resume.name


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
