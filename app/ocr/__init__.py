"""Optional OCR support for scanned PDFs."""

from .ocr_engine import OCRUnavailableError, extract_page_text

__all__ = ["OCRUnavailableError", "extract_page_text"]
"""OCR-related modules."""
