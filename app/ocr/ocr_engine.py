"""Optional OCR support for scanned PDF pages."""

from __future__ import annotations

import os
from pathlib import Path

import fitz


class OCRUnavailableError(RuntimeError):
    """Raised when Python OCR support or Tesseract is unavailable."""


def _configure_tesseract(pytesseract) -> None:
    """Configure Tesseract from PATH or common Windows install locations."""
    candidates = [
        os.environ.get("TESSERACT_CMD", ""),
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            pytesseract.pytesseract.tesseract_cmd = candidate
            return

    try:
        pytesseract.get_tesseract_version()
    except Exception as exc:
        raise OCRUnavailableError(
            "OCR requires Tesseract OCR. Install it and add it to PATH, "
            "or set the TESSERACT_CMD environment variable."
        ) from exc


def extract_page_text(page: fitz.Page) -> str:
    """Extract text from a scanned PDF page with Tesseract OCR."""
    try:
        import pytesseract
        from PIL import Image
    except ImportError as exc:
        raise OCRUnavailableError(
            "OCR requires pytesseract and Pillow. Install the project requirements."
        ) from exc

    _configure_tesseract(pytesseract)
    pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
    image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
    return pytesseract.image_to_string(image).strip()
