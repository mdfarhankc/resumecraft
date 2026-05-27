"""Layout widgets - Row and Column."""

from __future__ import annotations

from dataclasses import dataclass, field

from docx.shared import Inches

from .base import BuildContext, Widget
from .helpers import clean_empty_first_paragraph, remove_table_borders, zero_table_cell_margins


@dataclass
class Column(Widget):
    """Vertical stack. Renders children sequentially into the container."""

    children: list[Widget] = field(default_factory=list)

    def build(self, ctx: BuildContext) -> None:
        for child in self.children:
            child.build(ctx)


@dataclass
class Row(Widget):
    """Horizontal layout using an invisible single-row table."""

    children: list[Widget] = field(default_factory=list)
    widths: list[float] | None = None  # column widths in inches, optional

    def build(self, ctx: BuildContext) -> None:
        if not self.children:
            return

        table = ctx.container.add_table(rows=1, cols=len(self.children))
        remove_table_borders(table)
        zero_table_cell_margins(table)
        table.autofit = False

        for i, child in enumerate(self.children):
            cell = table.cell(0, i)
            if self.widths and i < len(self.widths):
                cell.width = Inches(self.widths[i])
            child.build(ctx.with_container(cell))
            clean_empty_first_paragraph(cell)
