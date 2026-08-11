"""
loader.py

PDF loading and inspection utilities.

Responsibilities:
    - Open PDF documents.
    - Validate input files.
    - Read metadata.
    - Detect searchable vs scanned PDFs.
    - Provide access to PDF pages.

This module intentionally does NOT:
    - Render pages
    - Perform OCR
    - Update the UI
"""

from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass
from typing import Optional

import fitz  # PyMuPDF


# ---------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------

class PDFLoaderError(Exception):
    """Base exception for PDF loading errors."""


class PDFNotFoundError(PDFLoaderError):
    """Raised when the PDF file cannot be found."""


class InvalidPDFError(PDFLoaderError):
    """Raised when the file is not a valid PDF."""


# ---------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------

@dataclass(slots=True)
class PDFMetadata:
    title: str
    author: str
    subject: str
    keywords: str
    creator: str
    producer: str
    creation_date: str
    modification_date: str
    page_count: int


# ---------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------

class PDFLoader:
    """
    Opens and inspects PDF documents.

    Example
    -------
    loader = PDFLoader()

    loader.open("book.pdf")

    print(loader.page_count)

    metadata = loader.metadata

    print(metadata.title)
    """

    def __init__(self) -> None:
        self._document: Optional[fitz.Document] = None
        self._path: Optional[Path] = None

    # -------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------

    def open(self, file_path: str | Path) -> None:
        """
        Open a PDF document.

        Parameters
        ----------
        file_path
            Path to the PDF file.
        """

        path = Path(file_path)

        if not path.exists():
            raise PDFNotFoundError(f"PDF not found: {path}")

        if path.suffix.lower() != ".pdf":
            raise InvalidPDFError("Selected file is not a PDF.")

        try:
            self._document = fitz.open(path)
            self._path = path

        except Exception as exc:
            raise InvalidPDFError(str(exc)) from exc

    def close(self) -> None:
        """Close the current PDF."""

        if self._document is not None:
            self._document.close()

        self._document = None
        self._path = None

    # -------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------

    @property
    def is_open(self) -> bool:
        return self._document is not None

    @property
    def page_count(self) -> int:
        self._require_document()
        return self._document.page_count

    @property
    def path(self) -> Optional[Path]:
        return self._path

    @property
    def metadata(self) -> PDFMetadata:
        """
        Return document metadata.
        """

        self._require_document()

        meta = self._document.metadata

        return PDFMetadata(
            title=meta.get("title", ""),
            author=meta.get("author", ""),
            subject=meta.get("subject", ""),
            keywords=meta.get("keywords", ""),
            creator=meta.get("creator", ""),
            producer=meta.get("producer", ""),
            creation_date=meta.get("creationDate", ""),
            modification_date=meta.get("modDate", ""),
            page_count=self._document.page_count,
        )

    # -------------------------------------------------------------
    # Page Access
    # -------------------------------------------------------------

    def get_page(self, page_number: int) -> fitz.Page:
        """
        Return a page object.

        Parameters
        ----------
        page_number
            Zero-based page index.
        """

        self._require_document()

        if page_number < 0 or page_number >= self._document.page_count:
            raise IndexError("Page number out of range.")

        return self._document.load_page(page_number)

    # -------------------------------------------------------------
    # Searchability Detection
    # -------------------------------------------------------------

    def is_searchable(self, sample_pages: int = 5) -> bool:
        """
        Determine whether the PDF already contains selectable text.

        Only the first few pages are sampled for performance.
        """

        self._require_document()

        pages = min(sample_pages, self._document.page_count)

        for i in range(pages):
            page = self._document.load_page(i)

            text = page.get_text("text")

            if text.strip():
                return True

        return False

    # -------------------------------------------------------------
    # Internal
    # -------------------------------------------------------------

    def _require_document(self) -> None:
        if self._document is None:
            raise PDFLoaderError("No PDF document is currently open.")