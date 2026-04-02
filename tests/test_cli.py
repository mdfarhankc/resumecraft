import json
import re

import pytest

pytest.importorskip("typer", reason="CLI tests require typer (pip install resumecraft[cli])")

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
        # Should match resume_YYYY-MM-DD_HH-MMam/pm.docx
        files = list(tmp_path.glob("resume_*.docx"))
        assert len(files) == 1
        assert re.match(r"resume_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}(am|pm)\.docx", files[0].name)

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
