import json
import warnings

import pytest

from resumecraft import ResumeCraft


class TestFactories:
    def test_from_resume(self, minimal_resume):
        rc = ResumeCraft(minimal_resume)
        assert rc.resume is minimal_resume

    def test_from_dict(self, minimal_resume):
        rc = ResumeCraft.from_dict(minimal_resume.model_dump())
        assert rc.resume.name == "John Doe"

    def test_from_json_string(self, minimal_resume):
        s = json.dumps(minimal_resume.model_dump())
        rc = ResumeCraft.from_json(s)
        assert rc.resume.name == "John Doe"

    def test_from_jsonfile(self, sample_json_path):
        rc = ResumeCraft.from_jsonfile(sample_json_path)
        assert rc.resume.name

    def test_from_bytes(self, minimal_resume):
        s = json.dumps(minimal_resume.model_dump())
        rc = ResumeCraft.from_bytes(s.encode("utf-8"))
        assert rc.resume.name == "John Doe"

    def test_from_bytes_with_bom(self, minimal_resume):
        s = json.dumps(minimal_resume.model_dump())
        rc = ResumeCraft.from_bytes(b"\xef\xbb\xbf" + s.encode("utf-8"))
        assert rc.resume.name == "John Doe"

    def test_from_bytes_rejects_binary(self):
        with pytest.raises(ValueError, match="not valid UTF-8"):
            ResumeCraft.from_bytes(b"\x95\x00\x01garbage")


class TestDeprecatedConstructors:
    def test_dict_constructor_warns(self, minimal_resume):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            ResumeCraft(minimal_resume.model_dump())
            assert any(issubclass(x.category, DeprecationWarning) for x in w)

    def test_string_constructor_warns(self, minimal_resume):
        s = json.dumps(minimal_resume.model_dump())
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            ResumeCraft(s)
            assert any(issubclass(x.category, DeprecationWarning) for x in w)

    def test_from_json_path_warns(self, sample_json_path):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            ResumeCraft.from_json(sample_json_path)
            assert any(issubclass(x.category, DeprecationWarning) for x in w)


class TestRepr:
    def test_full(self, full_resume):
        rc = ResumeCraft(full_resume)
        assert "ResumeCraft(" in repr(rc)
        assert "Jane Smith" in repr(rc)

    def test_minimal(self, minimal_resume):
        rc = ResumeCraft(minimal_resume)
        assert "sections=1" in repr(rc)


class TestSampleAndSchema:
    def test_sample_is_valid(self):
        rc = ResumeCraft.from_dict(ResumeCraft.sample())
        assert rc.resume.name == "Your Name"

    def test_json_schema(self):
        schema = ResumeCraft.json_schema()
        assert schema["type"] == "object"
        assert "name" in schema["properties"]


class TestExports:
    def test_to_dict(self, full_resume):
        data = ResumeCraft(full_resume).to_dict()
        assert data["name"] == "Jane Smith"

    def test_roundtrip(self, full_resume):
        rc1 = ResumeCraft(full_resume)
        rc2 = ResumeCraft.from_dict(rc1.to_dict())
        assert rc1.resume.name == rc2.resume.name


class TestToDocx:
    def test_creates_file(self, minimal_resume, tmp_path):
        path = ResumeCraft(minimal_resume).to_docx(tmp_path / "out.docx")
        assert path.exists() and path.stat().st_size > 0

    def test_creates_parent_dirs(self, minimal_resume, tmp_path):
        path = ResumeCraft(minimal_resume).to_docx(tmp_path / "a" / "b" / "out.docx")
        assert path.exists()

    def test_full(self, full_resume, tmp_path):
        path = ResumeCraft(full_resume).to_docx(tmp_path / "full.docx")
        assert path.exists()


class TestToDocxBytes:
    def test_returns_bytes(self, minimal_resume):
        data = ResumeCraft(minimal_resume).to_docx_bytes()
        assert isinstance(data, bytes) and len(data) > 0
        assert data[:2] == b"PK"  # docx is a zip

    def test_to_bytes_deprecated(self, minimal_resume):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            data = ResumeCraft(minimal_resume).to_docx_bytes()  # ok, no warning
            assert not any(issubclass(x.category, DeprecationWarning) for x in w)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            ResumeCraft(minimal_resume).to_bytes()  # deprecated alias
            assert any(issubclass(x.category, DeprecationWarning) for x in w)
        assert isinstance(data, bytes)


class TestToPdf:
    def test_raises_without_docx2pdf(self, minimal_resume, tmp_path, monkeypatch):
        import sys
        monkeypatch.setitem(sys.modules, "docx2pdf", None)
        with pytest.raises(ImportError, match="docx2pdf"):
            ResumeCraft(minimal_resume).to_pdf(tmp_path / "x.pdf")

    def test_writes_output(self, minimal_resume, tmp_path, monkeypatch):
        import shutil
        import sys
        import types

        fake = types.ModuleType("docx2pdf")
        fake.convert = lambda src, dst: shutil.copy(src, dst)  # type: ignore
        monkeypatch.setitem(sys.modules, "docx2pdf", fake)

        out = tmp_path / "resume.pdf"
        ResumeCraft(minimal_resume).to_pdf(out)
        assert out.exists()
        assert not list(tmp_path.glob("*.docx"))

    def test_to_pdf_bytes(self, minimal_resume, tmp_path, monkeypatch):
        import shutil
        import sys
        import types

        fake = types.ModuleType("docx2pdf")
        fake.convert = lambda src, dst: shutil.copy(src, dst)  # type: ignore
        monkeypatch.setitem(sys.modules, "docx2pdf", fake)

        data = ResumeCraft(minimal_resume).to_pdf_bytes()
        assert isinstance(data, bytes) and len(data) > 0
