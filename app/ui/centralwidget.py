"""
Central workspace for the Proofreader application.

Layout

----------------------------------------------------------
|                |                                       |
|                |                                       |
|     PDF        |      Generated Word Document          |
|     Viewer     |      Preview / Editor                 |
|                |                                       |
|                |                                       |
----------------------------------------------------------

Future:
    Left  -> PyMuPDF Viewer
    Right -> Rich Document Editor
"""

import fitz
from typing import Dict

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QImage, QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QSplitter,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QFrame,
    QSizePolicy,
    QComboBox,
)

from app.model.document import BlockType, DocumentBlock


# ==========================================================
# PDF PANEL
# ==========================================================

class PdfViewerWidget(QFrame):
    """
    Placeholder for the PDF Viewer.

    Later this widget will contain:

    - PyMuPDF renderer
    - Zoom
    - Page navigation
    - OCR overlay
    - Bounding boxes
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout(self)

        title = QLabel("Source PDF")
        title.setAlignment(Qt.AlignCenter)

        font = QFont()
        font.setBold(True)
        font.setPointSize(11)

        title.setFont(font)

        self.viewer = QLabel()
        self.viewer.setAlignment(Qt.AlignCenter)
        self.viewer.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding,
        )
        self.viewer.setStyleSheet(
            "background-color: #ffffff; border: 1px solid #d0d0d0; color: #000000;"
        )

        self.source_editor = QTextEdit()
        self.source_editor.setReadOnly(True)
        self.source_editor.setStyleSheet(
            "background-color: #ffffff; color: #000000; border: 1px solid #d0d0d0;"
        )
        self.source_editor.hide()

        self.ocr_text = QTextEdit()
        self.ocr_text.setReadOnly(True)
        self.ocr_text.setMaximumHeight(140)
        self.ocr_text.setStyleSheet(
            "background-color: #ffffff; color: #000000; border: 1px solid #d0d0d0;"
        )
        self.ocr_text.hide()

        self.page_selector = QComboBox()

        self.viewer.setText("Open a PDF to begin.\n\nThe rendered pages will appear here.")

        layout.addWidget(title)
        layout.addWidget(self.page_selector)
        layout.addWidget(self.viewer)
        layout.addWidget(self.ocr_text)
        layout.addWidget(self.source_editor)

        self._document = None
        self._document_path = None
        self._pixmap_cache: Dict[int, QPixmap] = {}
        self._current_pixmap: QPixmap | None = None

    def set_document(self, document_model):
        self.viewer.show()
        self.source_editor.hide()
        self.ocr_text.hide()
        self._document = document_model
        self._document_path = document_model.source_path
        self._pixmap_cache.clear()
        self._current_pixmap = None
        self.page_selector.clear()

        if document_model and document_model.pages:
            for page in document_model.pages:
                self.page_selector.addItem(f"Page {page.number}")
            self.page_selector.setCurrentIndex(0)
            self._render_selected_page(0)
        else:
            self.viewer.clear()

    def _render_selected_page(self, index: int):
        if not self._document or not self._document.pages:
            return

        page = self._document.pages[index]
        if not self._document_path:
            return

        # Use cached pixmap when available
        if page.number in self._pixmap_cache:
            self._display_pixmap(self._pixmap_cache[page.number])
            return

        try:
            document = fitz.open(self._document_path)
            page_obj = document.load_page(page.number - 1)
            pix = page_obj.get_pixmap(matrix=fitz.Matrix(1.6, 1.6), alpha=True)

            # Choose appropriate QImage format depending on presence of alpha
            if pix.alpha:  # RGBA
                fmt = QImage.Format_RGBA8888
            else:
                fmt = QImage.Format_RGB888

            image = QImage(
                pix.samples,
                pix.width,
                pix.height,
                pix.stride,
                fmt,
            )

            pixmap = QPixmap.fromImage(image)

            # cache and display
            self._pixmap_cache[page.number] = pixmap
            self._display_pixmap(pixmap)
            ocr_blocks = [
                block.text
                for block in page.blocks
                if block.metadata.get("source") == "ocr"
            ]
            self.ocr_text.setPlainText("\n".join(ocr_blocks))
            self.ocr_text.setVisible(bool(ocr_blocks))

            document.close()
        except Exception:
            # Fallback to text if rendering fails
            text = getattr(page, "text", None) or "Unable to render this page"
            self.viewer.setText(text)
            self.ocr_text.setPlainText(text)
            self.ocr_text.show()

    def set_source_text(self, text: str) -> None:
        """Display imported DOCX text in the left source panel."""
        self._document = None
        self._document_path = None
        self._pixmap_cache.clear()
        self._current_pixmap = None
        self.page_selector.clear()
        self.viewer.hide()
        self.source_editor.show()
        self.source_editor.setPlainText(text)

    def _display_pixmap(self, pixmap: QPixmap) -> None:
        """Fit a rendered page inside the viewer without distorting it."""
        self._current_pixmap = pixmap
        available_size = self.viewer.size()
        if available_size.width() <= 0 or available_size.height() <= 0:
            return

        fitted = pixmap.scaled(
            available_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.viewer.setPixmap(fitted)

    def resizeEvent(self, event):
        """Keep the current page fitted when the panel is resized."""
        super().resizeEvent(event)
        if self._current_pixmap is not None:
            self._display_pixmap(self._current_pixmap)

    def render_page(self, index: int) -> QPixmap | None:
        """Render and return a page pixmap for another preview widget."""
        if not self._document or not self._document.pages:
            return None

        if index < 0 or index >= len(self._document.pages):
            return None

        page = self._document.pages[index]
        if page.number in self._pixmap_cache:
            return self._pixmap_cache[page.number]

        self._render_selected_page(index)
        return self._pixmap_cache.get(page.number)


# ==========================================================
# WORD PREVIEW PANEL
# ==========================================================

class DocumentPreviewWidget(QFrame):
    """
    Generated Word document preview.

    Eventually this will become a rich document editor
    driven by the internal DocumentModel.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout(self)

        title = QLabel("Generated Word Document")
        title.setAlignment(Qt.AlignCenter)

        font = QFont()
        font.setBold(True)
        font.setPointSize(11)

        title.setFont(font)

        self.editor = QTextEdit()
        self.editor.setAcceptRichText(False)
        self.editor.setStyleSheet(
            "background-color: #ffffff; color: #000000; border: 1px solid #d0d0d0;"
        )
        self.editor.setPlaceholderText("The editable output will appear here.")
        self.editor.textChanged.connect(self._save_current_page_text)

        self.page_selector = QComboBox()

        layout.addWidget(title)
        layout.addWidget(self.page_selector)
        layout.addWidget(self.editor)

        self._document = None
        self._current_page_index = -1
        self._loading_page = False

    def set_document(self, document_model):
        self._document = document_model
        self._current_page_index = -1
        self.page_selector.clear()

        if document_model and document_model.pages:
            for page in document_model.pages:
                self.page_selector.addItem(f"Page {page.number}")
            self.page_selector.setCurrentIndex(0)
            self._show_selected_page(0)
        else:
            self.editor.clear()

    def _show_selected_page(self, index: int):
        if not self._document or not self._document.pages:
            return

        if index < 0 or index >= len(self._document.pages):
            return

        self._current_page_index = index
        page = self._document.pages[index]
        self._loading_page = True
        self.editor.setPlainText(page.text)
        self._loading_page = False

    def _save_current_page_text(self):
        """Write user edits from the output panel back to the model."""
        if self._loading_page or not self._document:
            return
        if 0 <= self._current_page_index < len(self._document.pages):
            page = self._document.pages[self._current_page_index]
            lines = self.editor.toPlainText().splitlines()
            page.blocks[:] = [
                DocumentBlock(
                    type=BlockType.PARAGRAPH,
                    text=line,
                    confidence=1.0,
                    metadata={"source": "user"},
                )
                for line in lines
                if line.strip()
            ]


# ==========================================================
# CENTRAL WIDGET
# ==========================================================

class CentralWidget(QWidget):
    """
    Main application workspace.

    Left:
        Source PDF

    Right:
        Generated document
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._build_ui()
        self._selectors_connected = False

    # ------------------------------------------------------

    def _build_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(4, 4, 4, 4)

        self.splitter = QSplitter(Qt.Horizontal)

        self.pdf_panel = PdfViewerWidget()

        self.document_panel = DocumentPreviewWidget()

        self.pdf_panel.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        self.document_panel.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        self.splitter.addWidget(self.pdf_panel)

        self.splitter.addWidget(self.document_panel)

        #
        # Give both panels equal width
        #

        self.splitter.setStretchFactor(0, 1)

        self.splitter.setStretchFactor(1, 1)

        self.splitter.setChildrenCollapsible(False)

        layout.addWidget(self.splitter)

    # ======================================================
    # Public API
    # ======================================================

    def set_pdf_text(self, text: str):
        """Update the PDF text view."""
        self.pdf_panel.viewer.setText(text)

    def set_document_text(self, text: str):
        """Retained for compatibility; output is rendered page content."""
        if not self.document_panel._document:
            self.document_panel.editor.setPlainText(text)

    def set_document_model(self, document_model):
        """Render the document model into both panels."""
        self.pdf_panel.set_document(document_model)
        self.document_panel.set_document(document_model)
        # Connect selectors once to keep them synchronized
        if not getattr(self, "_selectors_connected", False):
            self.pdf_panel.page_selector.currentIndexChanged.connect(self.sync_page)
            self.document_panel.page_selector.currentIndexChanged.connect(self.sync_page)
            self._selectors_connected = True

    @property
    def document_model(self):
        """Return the currently loaded editable document model."""
        return self.document_panel._document

    def sync_page(self, index: int):
        """Keep both selectors and both page previews on the same page."""
        if index < 0:
            return

        self.pdf_panel.page_selector.blockSignals(True)
        self.document_panel.page_selector.blockSignals(True)
        self.pdf_panel.page_selector.setCurrentIndex(index)
        self.document_panel.page_selector.setCurrentIndex(index)
        self.pdf_panel.page_selector.blockSignals(False)
        self.document_panel.page_selector.blockSignals(False)

        self.pdf_panel._render_selected_page(index)
        self.document_panel._show_selected_page(index)

        main_window = self.window()
        if hasattr(main_window, "status") and self.document_model:
            main_window.status.set_page(index + 1, self.document_model.page_count)

    def clear(self):
        """
        Clear both panes.
        """
        self.pdf_panel.viewer.clear()
        self.document_panel.editor.clear()