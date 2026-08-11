from pathlib import Path

import fitz

from app.core.pipeline import process_pdf


def test_process_pdf_extracts_text(tmp_path: Path) -> None:
    pdf_path = tmp_path / "sample.pdf"

    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "Hello OCR proofreader")
    document.save(pdf_path)
    document.close()

    result = process_pdf(pdf_path)

    assert "Hello OCR proofreader" in result["text"]
    assert result["metadata"]["page_count"] == 1
