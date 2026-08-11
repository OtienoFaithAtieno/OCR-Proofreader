"""
Core document object model for the OCR Proofreading Application.

This module contains the in-memory representation of a document.
Every subsystem (PDF import, OCR, layout analysis, proofreading,
and export) should read from and write to this model.

The model is intentionally independent of the UI and OCR engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import uuid4


# ----------------------------------------------------------------------
# Enumerations
# ----------------------------------------------------------------------

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    TABLE = "table"
    IMAGE = "image"
    FOOTNOTE = "footnote"
    CAPTION = "caption"
    LIST = "list"
    CODE = "code"
    UNKNOWN = "unknown"


# ----------------------------------------------------------------------
# Geometry
# ----------------------------------------------------------------------

@dataclass(slots=True)
class BoundingBox:
    """
    Rectangle in page coordinates.
    """

    x: float
    y: float
    width: float
    height: float

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height


# ----------------------------------------------------------------------
# OCR
# ----------------------------------------------------------------------

@dataclass(slots=True)
class OCRWord:
    text: str
    confidence: float
    bbox: BoundingBox


@dataclass(slots=True)
class OCRLine:
    words: List[OCRWord] = field(default_factory=list)

    @property
    def text(self) -> str:
        return " ".join(word.text for word in self.words)


# ----------------------------------------------------------------------
# Document Blocks
# ----------------------------------------------------------------------

@dataclass(slots=True)
class DocumentBlock:
    """
    Generic content block.
    """

    id: str = field(default_factory=lambda: str(uuid4()))

    type: BlockType = BlockType.UNKNOWN

    text: str = ""

    bbox: Optional[BoundingBox] = None

    confidence: float = 1.0

    style: Dict[str, str] = field(default_factory=dict)

    metadata: Dict[str, str] = field(default_factory=dict)


# ----------------------------------------------------------------------
# Images
# ----------------------------------------------------------------------

@dataclass(slots=True)
class ImageObject:

    id: str = field(default_factory=lambda: str(uuid4()))

    path: Optional[str] = None

    caption: str = ""

    bbox: Optional[BoundingBox] = None


# ----------------------------------------------------------------------
# Tables
# ----------------------------------------------------------------------

@dataclass(slots=True)
class TableCell:

    row: int

    column: int

    text: str


@dataclass(slots=True)
class TableObject:

    id: str = field(default_factory=lambda: str(uuid4()))

    cells: List[TableCell] = field(default_factory=list)

    bbox: Optional[BoundingBox] = None


# ----------------------------------------------------------------------
# Page
# ----------------------------------------------------------------------

@dataclass(slots=True)
class Page:

    number: int

    width: float

    height: float

    image_path: Optional[str] = None

    blocks: List[DocumentBlock] = field(default_factory=list)

    tables: List[TableObject] = field(default_factory=list)

    images: List[ImageObject] = field(default_factory=list)

    ocr_lines: List[OCRLine] = field(default_factory=list)

    metadata: Dict[str, str] = field(default_factory=dict)

    @property
    def text(self) -> str:
        """
        Entire page text.
        """
        return "\n".join(block.text for block in self.blocks)

    def add_block(self, block: DocumentBlock) -> None:
        """Append a content block to the page."""
        self.blocks.append(block)


# ----------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------

@dataclass(slots=True)
class DocumentMetadata:

    title: str = ""

    author: str = ""

    subject: str = ""

    keywords: List[str] = field(default_factory=list)

    creator: str = ""

    producer: str = ""

    language: str = "en"

    created: Optional[datetime] = None

    modified: Optional[datetime] = None


# ----------------------------------------------------------------------
# Root Document
# ----------------------------------------------------------------------

@dataclass(slots=True)
class Document:
    """
    Root document object.
    """

    id: str = field(default_factory=lambda: str(uuid4()))

    filename: str = ""

    source_path: str = ""

    metadata: DocumentMetadata = field(default_factory=DocumentMetadata)

    pages: List[Page] = field(default_factory=list)

    styles: Dict[str, Dict] = field(default_factory=dict)

    properties: Dict[str, str] = field(default_factory=dict)

    created: datetime = field(default_factory=datetime.utcnow)

    modified: datetime = field(default_factory=datetime.utcnow)

    # ----------------------------------------------------------

    @property
    def page_count(self) -> int:
        return len(self.pages)

    # ----------------------------------------------------------

    def add_page(self, page: Page) -> None:
        self.pages.append(page)
        self.modified = datetime.utcnow()

    # ----------------------------------------------------------

    def get_page(self, page_number: int) -> Optional[Page]:

        if 1 <= page_number <= len(self.pages):
            return self.pages[page_number - 1]

        return None

    # ----------------------------------------------------------

    def clear(self) -> None:

        self.pages.clear()

        self.styles.clear()

    def to_text(self) -> str:
        """Join the text of all pages into a single document text."""
        return "\n\n".join(page.text for page in self.pages if page.text)

        self.properties.clear()

        self.modified = datetime.utcnow()

    # ----------------------------------------------------------

    @property
    def full_text(self) -> str:

        return "\n\n".join(page.text for page in self.pages)

    # ----------------------------------------------------------

    def statistics(self) -> Dict[str, int]:

        blocks = sum(len(page.blocks) for page in self.pages)

        tables = sum(len(page.tables) for page in self.pages)

        images = sum(len(page.images) for page in self.pages)

        words = len(self.full_text.split())

        return {
            "pages": self.page_count,
            "blocks": blocks,
            "tables": tables,
            "images": images,
            "words": words,
        }