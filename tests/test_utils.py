import re

from resumecraft.utils import build_bold_pattern


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
