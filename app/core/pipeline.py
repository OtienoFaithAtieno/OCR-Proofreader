"""Simple document processing pipeline for PDFs."""

from pathlib import Path

from app.model.document import Document, DocumentMetadata, Page as DocumentPage, DocumentBlock, BlockType
from app.ocr.ocr_engine import run_ocr
from app.pdf.loader import PDFLoader


def process_pdf(document_path: str | Path) -> dict:
    """Open a PDF, extract text, and return metadata for the UI."""
    path = Path(document_path)
    loader = PDFLoader()
    loader.open(path)

    try:
        metadata = loader.metadata
        searchable = loader.is_searchable(sample_pages=3)

        if searchable:
            pages: list[DocumentPage] = []
            text_chunks: list[str] = []

            for page_number in range(loader.page_count):
                page = loader.get_page(page_number)
                text = page.get_text("text").strip()
                text_chunks.append(text)

                blocks = []
                if text:
                    for line in text.splitlines():
                        stripped = line.strip()
                        if stripped:
                            blocks.append(
                                DocumentBlock(
                                    type=BlockType.PARAGRAPH,
                                    text=stripped,
                                    confidence=0.95,
                                    metadata={"source": "pdf"},
                                )
                            )

                doc_page = DocumentPage(
                    number=page_number + 1,
                    width=float(page.rect.width),
                    height=float(page.rect.height),
                    metadata={"source": "pdf"},
                )
                doc_page.blocks = blocks
                pages.append(doc_page)

            document_model = Document(
                filename=path.name,
                source_path=str(path),
                metadata=DocumentMetadata(
                    title=metadata.title or path.stem,
                    author=metadata.author,
                    language="en",
                ),
                pages=pages,
            )
            text = "\n\n".join(chunk for chunk in text_chunks if chunk)
        else:
            ocr_result = run_ocr(path)
            document_model = ocr_result["document"]
            text = ocr_result["text"]

        return {
            "document": document_model,
            "text": text,
            "metadata": {
                "title": document_model.metadata.title,
                "author": document_model.metadata.author,
                "page_count": document_model.page_count,
                "path": str(path),
                "is_searchable": searchable,
            },
        }
    finally:
        loader.close()


def run_pipeline(document_path: str | Path) -> dict:
    """Compatibility wrapper for the old pipeline name."""
    return process_pdf(document_path)
