from pathlib import Path

import fitz
from PySide6.QtWidgets import QApplication

from app.core.pipeline import process_pdf
from app.ui.centralwidget import CentralWidget


def test_page_selection_syncs_and_preserves_edits(tmp_path: Path):
    app = QApplication.instance() or QApplication([])
    pdf_path = tmp_path / "pages.pdf"

    pdf = fitz.open()
    for page_number in range(2):
        page = pdf.new_page()
        page.insert_text((72, 72), f"Page {page_number + 1}")
    pdf.save(pdf_path)
    pdf.close()

    widget = CentralWidget()
    widget.set_document_model(process_pdf(pdf_path)["document"])
    widget.sync_page(1)
    widget.document_panel.editor.setPlainText("Edited page 2")
    widget.sync_page(0)
    widget.sync_page(1)

    assert widget.pdf_panel.page_selector.currentIndex() == 1
    assert widget.document_panel.page_selector.currentIndex() == 1
    assert widget.document_panel.editor.toPlainText() == "Edited page 2"

    widget.close()
    app.quit()
