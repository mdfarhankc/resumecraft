import json
import re

import pytest
from typer.testing import CliRunner

from resumecraft.cli import app

runner = CliRunner()


class TestVersion:
    def test_version_flag(self):
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "resumecraft" in result.output

    def test_version_short_flag(self):
        result = runner.invoke(app, ["-v"])
        assert result.exit_code == 0
        assert "resumecraft" in result.output


class TestBuild:
    def test_build_creates_docx(self, sample_json_path, tmp_path):
        output = tmp_path / "out.docx"
        result = runner.invoke(app, ["build", str(sample_json_path), "-o", str(output)])
        assert result.exit_code == 0
        assert "Resume saved to" in result.output
        assert output.exists()

    def test_build_default_output_has_timestamp(self, sample_json_path, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["build", str(sample_json_path)])
        assert result.exit_code == 0
        assert "Resume saved to" in result.output
        stem = sample_json_path.stem
        files = list(tmp_path.glob(f"{stem}_*.docx"))
        assert len(files) == 1
        assert re.match(
            rf"{re.escape(stem)}_\d{{4}}-\d{{2}}-\d{{2}}_\d{{2}}-\d{{2}}(am|pm)\.docx",
            files[0].name,
        )

    def test_build_file_not_found(self):
        result = runner.invoke(app, ["build", "nonexistent.json"])
        assert result.exit_code == 1
        assert "not found" in result.output

    def test_build_invalid_json(self, tmp_path):
        bad = tmp_path / "bad.json"
        bad.write_text("{broken", encoding="utf-8")
        result = runner.invoke(app, ["build", str(bad)])
        assert result.exit_code == 1
        assert "Invalid JSON" in result.output

    def test_build_invalid_data(self, tmp_path):
        bad = tmp_path / "bad.json"
        bad.write_text('{"name": 123}', encoding="utf-8")
        result = runner.invoke(app, ["build", str(bad)])
        assert result.exit_code == 1
        assert "Invalid resume data" in result.output

    def test_build_non_json_extension(self, tmp_path):
        txt = tmp_path / "resume.txt"
        txt.write_text("not json", encoding="utf-8")
        result = runner.invoke(app, ["build", str(txt)])
        assert result.exit_code == 1
        assert "must be a .json" in result.output

    def test_build_binary_input(self, tmp_path):
        # Rename a binary to .json to bypass the extension check
        bad = tmp_path / "bad.json"
        bad.write_bytes(b"\x95\x00\x01\x02garbage")
        result = runner.invoke(app, ["build", str(bad)])
        assert result.exit_code == 1
        assert "not a valid UTF-8" in result.output

    def test_build_output_is_directory(self, sample_json_path, tmp_path):
        result = runner.invoke(app, ["build", str(sample_json_path), "-o", str(tmp_path)])
        assert result.exit_code == 1
        assert "is a directory" in result.output

    def test_build_yaml_input(self, sample_json_path, tmp_path):
        import json

        import yaml
        data = json.loads(sample_json_path.read_text(encoding="utf-8"))
        yaml_path = tmp_path / "resume.yaml"
        yaml_path.write_text(yaml.safe_dump(data))
        out = tmp_path / "out.docx"
        result = runner.invoke(app, ["build", str(yaml_path), "-o", str(out)])
        assert result.exit_code == 0
        assert out.exists()

    def test_build_pdf_flag_uses_input_stem(self, sample_json_path, tmp_path, monkeypatch):
        # Stub docx2pdf to avoid requiring Word
        import shutil
        import sys
        import types
        fake = types.ModuleType("docx2pdf")
        fake.convert = lambda src, dst: shutil.copy(src, dst)
        monkeypatch.setitem(sys.modules, "docx2pdf", fake)

        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["build", str(sample_json_path), "--pdf"])
        assert result.exit_code == 0
        assert (tmp_path / f"{sample_json_path.stem}.pdf").exists()


class TestValidate:
    def test_validate_valid_file(self, sample_json_path):
        result = runner.invoke(app, ["validate", str(sample_json_path)])
        assert result.exit_code == 0
        assert "Valid" in result.output

    def test_validate_file_not_found(self):
        result = runner.invoke(app, ["validate", "nonexistent.json"])
        assert result.exit_code == 1
        assert "not found" in result.output

    def test_validate_invalid_json(self, tmp_path):
        bad = tmp_path / "bad.json"
        bad.write_text("{nope", encoding="utf-8")
        result = runner.invoke(app, ["validate", str(bad)])
        assert result.exit_code == 1
        assert "Invalid JSON" in result.output

    def test_validate_missing_fields(self, tmp_path):
        bad = tmp_path / "incomplete.json"
        bad.write_text('{"name": "Test"}', encoding="utf-8")
        result = runner.invoke(app, ["validate", str(bad)])
        assert result.exit_code == 1
        assert "contact" in result.output
        assert "summary" in result.output


class TestInit:
    def test_init_creates_template(self, tmp_path):
        output = tmp_path / "template.json"
        result = runner.invoke(app, ["init", "-o", str(output)])
        assert result.exit_code == 0
        assert "Template saved to" in result.output
        assert output.exists()

        data = json.loads(output.read_text(encoding="utf-8"))
        assert "name" in data
        assert "contact" in data
        assert "summary" in data

    def test_init_template_is_valid(self, tmp_path):
        output = tmp_path / "template.json"
        runner.invoke(app, ["init", "-o", str(output)])

        # The generated template should pass validation
        result = runner.invoke(app, ["validate", str(output)])
        assert result.exit_code == 0


class TestBuildPdfFlow:
    def test_build_pdf_without_docx2pdf(self, sample_json_path, tmp_path, monkeypatch):
        import sys
        monkeypatch.setitem(sys.modules, "docx2pdf", None)
        result = runner.invoke(app, ["build", str(sample_json_path), "-o", str(tmp_path / "x.pdf")])
        assert result.exit_code == 1
        assert "docx2pdf" in result.output


class TestWatchMode:
    def test_watch_file_not_found(self):
        pytest.importorskip("watchfiles")
        result = runner.invoke(app, ["watch", "nonexistent.json"])
        assert result.exit_code == 1
        assert "not found" in result.output

    def test_watch_without_watchfiles(self, sample_json_path, monkeypatch):
        import sys
        monkeypatch.setitem(sys.modules, "watchfiles", None)
        result = runner.invoke(app, ["watch", str(sample_json_path)])
        assert result.exit_code == 1
        assert "watchfiles" in result.output


def test_open_file_windows(monkeypatch):
    import sys as _sys

    from resumecraft import cli
    calls: list[object] = []
    monkeypatch.setattr(_sys, "platform", "win32")
    monkeypatch.setattr(cli.os, "startfile", lambda p: calls.append(p), raising=False)
    cli._open_file(cli.Path("x.docx"))
    assert len(calls) == 1


@pytest.mark.parametrize("system,expected_cmd", [
    ("Darwin", "open"),
    ("Linux", "xdg-open"),
])
def test_open_file_unix(monkeypatch, system, expected_cmd):
    import sys as _sys

    from resumecraft import cli
    calls = []
    monkeypatch.setattr(_sys, "platform", "linux")
    monkeypatch.setattr(cli.platform, "system", lambda: system)
    monkeypatch.setattr(cli.subprocess, "Popen", lambda *a, **kw: calls.append(a))
    cli._open_file(cli.Path("x.docx"))
    assert calls[0][0][0] == expected_cmd
