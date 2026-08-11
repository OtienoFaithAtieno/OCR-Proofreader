from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .paragraph import Paragraph
from .table import Table
from .image import ImageElement


@dataclass
class Page:
    """
    Represents a single page in the document.
    """

    page_number: int

    width: float
    height: float

    rotation: int = 0

    source_image: Optional[str] = None

    paragraphs: List[Paragraph] = field(default_factory=list)

    tables: List[Table] = field(default_factory=list)

    images: List[ImageElement] = field(default_factory=list)

    header: Optional[Paragraph] = None

    footer: Optional[Paragraph] = None

    ocr_complete: bool = False

    confidence: float = 0.0

    metadata: dict = field(default_factory=dict)

    @property
    def text(self) -> str:
        return "\n".join(p.text for p in self.paragraphs)

    def add_paragraph(self, paragraph: Paragraph):
        self.paragraphs.append(paragraph)

    def add_table(self, table: Table):
        self.tables.append(table)

    def add_image(self, image: ImageElement):
        self.images.append(image)