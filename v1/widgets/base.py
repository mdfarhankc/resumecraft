"""Widget base class and build context."""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, replace
from typing import Any

from ..templates.base import Template


@dataclass(frozen=True)
class BuildContext:
    """Immutable rendering state passed down the widget tree."""

    doc: Any
    container: Any
    template: Template = field(default_factory=Template)
    font_name: str = "Calibri"
    font_size: float = 10
    font_color: str | None = None
    bold_pattern: re.Pattern[str] | None = None
    is_first_entry: bool = True

    def with_container(self, container: Any) -> BuildContext:
        """Return a copy targeting a different container (e.g. a table cell)."""
        return replace(self, container=container)

    def with_font(
        self,
        name: str | None = None,
        size: float | None = None,
        color: str | None = None,
    ) -> BuildContext:
        """Return a copy with overridden font defaults for child widgets."""
        return replace(
            self,
            font_name=name or self.font_name,
            font_size=size or self.font_size,
            font_color=color if color is not None else self.font_color,
        )

    def with_entry_position(self, *, is_first: bool) -> BuildContext:
        """Return a copy with updated entry position flag."""
        return replace(self, is_first_entry=is_first)


class Widget(ABC):
    """Base class for all resume widgets."""

    @abstractmethod
    def build(self, ctx: BuildContext) -> None: ...
