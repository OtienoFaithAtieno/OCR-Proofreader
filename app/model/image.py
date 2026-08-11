from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple


BoundingBox = Tuple[float, float, float, float]


@dataclass
class ImageElement:
    """
    Represents an image detected on a page.
    """

    id: int

    page: int

    bbox: BoundingBox

    file_path: Optional[str] = None

    caption: str = ""

    alt_text: str = ""

    width: float = 0

    height: float = 0

    dpi: int = 300

    confidence: float = 0.0

    metadata: dict = field(default_factory=dict)

    @property
    def has_caption(self) -> bool:
        return bool(self.caption.strip())