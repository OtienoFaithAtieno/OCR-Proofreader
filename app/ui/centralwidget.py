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

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget,
    QSplitter,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QFrame,
    QSizePolicy,
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

        self.viewer = QTextEdit()

        self.viewer.setReadOnly(True)

        self.viewer.setPlaceholderText(
            "Open a PDF to begin.\n\n"
            "The original scanned document will appear here."
        )

        layout.addWidget(title)
        layout.addWidget(self.viewer)


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

        self.editor.setPlaceholderText(
            "Processed document will appear here..."
        )

        layout.addWidget(title)
        layout.addWidget(self.editor)


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
        """
        Temporary helper.

        Later this will load rendered PDF pages.
        """
        self.pdf_panel.viewer.setPlainText(text)

    def set_document_text(self, text: str):
        """
        Update generated document preview.
        """
        self.document_panel.editor.setPlainText(text)

    def clear(self):
        """
        Clear both panes.
        """
        self.pdf_panel.viewer.clear()
        self.document_panel.editor.clear()