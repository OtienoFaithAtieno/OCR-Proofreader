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
        self.viewer.setMinimumHeight(320)
        self.viewer.setStyleSheet(
            "background-color: #f5f5f5; border: 1px solid #d0d0d0;"
        )

        self.page_selector = QComboBox()
        self.page_selector.currentIndexChanged.connect(self._render_selected_page)

        self.viewer.setText("Open a PDF to begin.\n\nThe rendered pages will appear here.")

        layout.addWidget(title)
        layout.addWidget(self.page_selector)
        layout.addWidget(self.viewer)

        self._document = None
        self._document_path = None

    def set_document(self, document_model):
        self._document = document_model
        self._document_path = document_model.source_path
        self.page_selector.clear()

        if document_model and document_model.pages:
            for page in document_model.pages:
                self.page_selector.addItem(f"Page {page.number}")
            self.page_selector.setCurrentIndex(0)
            self._render_selected_page(0)
        else:
            self.viewer.setText("No pages available")

    def _render_selected_page(self, index: int):
        if not self._document or not self._document.pages:
            return

        page = self._document.pages[index]
        if not self._document_path:
            return

        try:
            document = fitz.open(self._document_path)
            page_obj = document.load_page(page.number - 1)
            pix = page_obj.get_pixmap(matrix=fitz.Matrix(1.6, 1.6), alpha=False)
            image = QImage(
                pix.samples,
                pix.width,
                pix.height,
                pix.stride,
                QImage.Format_RGB888,
            )
            self.viewer.setPixmap(QPixmap.fromImage(image))
            document.close()
        except Exception:
            self.viewer.setText("Unable to render this page")


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
        self.editor.setLineWrapMode(QTextEdit.NoWrap)

        self.editor.setPlaceholderText(
            "Processed document preview will appear here..."
        )

        self.page_selector = QComboBox()
        self.page_selector.currentIndexChanged.connect(self._show_selected_page)

        layout.addWidget(title)
        layout.addWidget(self.page_selector)
        layout.addWidget(self.editor)

        self._document = None

    def set_document(self, document_model):
        self._document = document_model
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

        page = self._document.pages[index]
        if page.text:
            self.editor.setPlainText(page.text)
        else:
            self.editor.setPlainText("This page contains no extracted text")


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
        """Update generated document preview."""
        self.document_panel.editor.setPlainText(text)

    def set_document_model(self, document_model):
        """Render the document model into both panels."""
        self.pdf_panel.set_document(document_model)
        self.document_panel.set_document(document_model)

    def clear(self):
        """
        Clear both panes.
        """
        self.pdf_panel.viewer.clear()
        self.document_panel.editor.clear()