from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple


BoundingBox = Tuple[float, float, float, float]


@dataclass
class TableCell:

    row: int

    column: int

    text: str

    rowspan: int = 1

    colspan: int = 1

    confidence: float = 0.0


@dataclass
class Table:

    id: int

    page: int

    bbox: BoundingBox

    rows: int

    columns: int

    cells: List[TableCell] = field(default_factory=list)

    title: str = ""

    confidence: float = 0.0

    metadata: dict = field(default_factory=dict)

    def add_cell(self, cell: TableCell):
        self.cells.append(cell)

    def get_cell(self, row: int, column: int):

        for cell in self.cells:
            if cell.row == row and cell.column == column:
                return cell

        return None