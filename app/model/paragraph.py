from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


BoundingBox = Tuple[float, float, float, float]


@dataclass
class Paragraph:
    """
    Represents one logical paragraph detected from OCR.
    """

    id: int

    text: str

    bbox: BoundingBox

    page: int

    style: str = "Normal"

    heading_level: int = 0

    font_name: str = ""

    font_size: float = 0

    bold: bool = False

    italic: bool = False

    underline: bool = False

    confidence: float = 0.0

    language: str = "en"

    alignment: str = "left"

    metadata: dict = field(default_factory=dict)

    @property
    def is_heading(self) -> bool:
        return self.heading_level > 0

    @property
    def word_count(self) -> int:
        return len(self.text.split())