import io
import re
import urllib.error

import pytest

from resumecraft.utils import build_bold_pattern, load_photo_image


class TestBuildBoldPattern:
    def test_returns_none_for_empty_list(self):
        assert build_bold_pattern([]) is None

    def test_returns_compiled_pattern(self):
        pattern = build_bold_pattern(["Python", "React"])
        assert isinstance(pattern, re.Pattern)

    def test_matches_keywords(self):
        pattern = build_bold_pattern(["Python", "React"])
        parts = pattern.split("Built APIs using Python and React.")
        assert "Python" in parts
        assert "React" in parts

    def test_longer_keywords_matched_first(self):
        pattern = build_bold_pattern(["API", "REST API"])
        parts = pattern.split("Built a REST API for the project.")
        assert "REST API" in parts

    def test_special_characters_escaped(self):
        pattern = build_bold_pattern(["C++", "Node.js"])
        parts = pattern.split("Used C++ and Node.js together.")
        assert "C++" in parts
        assert "Node.js" in parts


class TestLoadPhotoImage:
    def test_loads_local_file(self, tmp_path):
        from tests.conftest import MINIMAL_PNG
        img = tmp_path / "photo.png"
        img.write_bytes(MINIMAL_PNG)
        result = load_photo_image(str(img))
        assert isinstance(result, io.BytesIO)
        assert len(result.getvalue()) > 0

    def test_raises_for_missing_file(self):
        with pytest.raises(ValueError, match="not found"):
            load_photo_image("/nonexistent/photo.jpg")

    def test_loads_from_url(self, monkeypatch):
        from tests.conftest import MINIMAL_PNG
        monkeypatch.setattr(
            "resumecraft.utils.urllib.request.urlopen",
            lambda url, timeout=None: io.BytesIO(MINIMAL_PNG),
        )
        result = load_photo_image("https://example.com/photo.png")
        assert isinstance(result, io.BytesIO)
        assert len(result.getvalue()) > 0

    def test_raises_for_http_error(self, monkeypatch):
        def _raise(*a, **kw):
            raise urllib.error.HTTPError("https://x.com/404.png", 404, "Not Found", {}, None)
        monkeypatch.setattr("resumecraft.utils.urllib.request.urlopen", _raise)
        with pytest.raises(ValueError, match="HTTP 404"):
            load_photo_image("https://x.com/404.png")

    def test_raises_for_url_error(self, monkeypatch):
        def _raise(*a, **kw):
            raise urllib.error.URLError("Connection refused")
        monkeypatch.setattr("resumecraft.utils.urllib.request.urlopen", _raise)
        with pytest.raises(ValueError, match="Connection refused"):
            load_photo_image("https://x.com/photo.png")
