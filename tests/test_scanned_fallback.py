from pathlib import Path

import fitz

from app.core import pipeline


def test_scanned_page_uses_fallback_only_when_text_is_missing(tmp_path: Path, monkeypatch):
    pdf_path = tmp_path / "scanned.pdf"
    pdf = fitz.open()
    page = pdf.new_page()
    pdf.save(pdf_path)
    pdf.close()

    monkeypatch.setattr(pipeline, "extract_page_text", lambda page: "Scanned text")
    result = pipeline.process_pdf(pdf_path)

    assert result["text"] == "Scanned text"
    assert result["document"].pages[0].blocks[0].text == "Scanned text"
