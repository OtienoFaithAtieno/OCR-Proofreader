"""Simple OCR fallback using PyMuPDF text extraction."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import fitz

from app.model.document import Document, DocumentMetadata, Page as DocumentPage
from app.model.paragraph import Paragraph


def run_ocr(document_path: str | Path) -> dict[str, Any]:
    """Extract text from a PDF using PyMuPDF as a lightweight OCR fallback."""
    path = Path(document_path)
    document = fitz.open(path)

    try:
        pages: list[DocumentPage] = []
        for page_number in range(document.page_count):
            page = document.load_page(page_number)
            text = page.get_text("text").strip()
            paragraphs: list[Paragraph] = []
            if text:
                for line in text.splitlines():
                    stripped = line.strip()
                    if stripped:
                        paragraphs.append(
                            Paragraph(
                                id=len(paragraphs) + 1,
                                text=stripped,
                                bbox=(0.0, 0.0, 0.0, 0.0),
                                page=page_number + 1,
                                confidence=0.9,
                            )
                        )
            doc_page = DocumentPage(
                page_number=page_number + 1,
                width=float(page.rect.width),
                height=float(page.rect.height),
                ocr_complete=True,
                confidence=0.9 if text else 0.0,
                metadata={"source": "fitz"},
            )
            doc_page.paragraphs = paragraphs
            pages.append(doc_page)

        metadata = DocumentMetadata(
            title=path.stem,
            author="",
            language="en",
        )

        document_model = Document(
            filename=path.name,
            source_path=str(path),
            metadata=metadata,
            pages=pages,
        )
        return {"document": document_model, "text": "\n\n".join(page.text for page in pages)}
    finally:
        document.close()
