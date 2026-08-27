"""
Application status bar.

Displays application status, page information,
OCR progress and document statistics.
"""


from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QProgressBar,
    QStatusBar,
)


class StatusBar(QStatusBar):
    """Custom application status bar."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("ApplicationStatusBar")
        self.setSizeGripEnabled(False)
        self.setStyleSheet(
            """
            QStatusBar {
                background: #2f2f2f;
                color: #f5f5f5;
                border-top: 1px solid #5a5a5a;
                padding: 2px 8px;
            }
            QStatusBar QLabel {
                color: #f5f5f5;
            }
            QStatusBar QProgressBar {
                border: 1px solid #666666;
                background: #222222;
                color: #f5f5f5;
            }
            """
        )

        self._create_widgets()

    # ---------------------------------------------------------

    def _create_widgets(self):

        #
        # Left message
        #

        self.showMessage("Ready")

        #
        # Page indicator
        #

        self.page_label = QLabel("Page: -- / --")

        #
        # Zoom
        #

        self.zoom_label = QLabel("Zoom: 100%")

        #
        # Document statistics
        #

        self.words_label = QLabel("Words: 0")

        #
        # Processing progress
        #

        self.progress = QProgressBar()

        self.progress.setFixedWidth(160)

        self.progress.setMinimum(0)

        self.progress.setMaximum(100)

        self.progress.setValue(0)

        self.progress.setTextVisible(True)

        #
        # Permanent widgets
        #

        self.addPermanentWidget(self.page_label)

        self.addPermanentWidget(self._separator())

        self.addPermanentWidget(self.zoom_label)

        self.addPermanentWidget(self._separator())

        self.addPermanentWidget(self.words_label)

        self.addPermanentWidget(self._separator())

        self.addPermanentWidget(self.progress)

    # ---------------------------------------------------------

    def _separator(self):

        label = QLabel(" | ")

        label.setAlignment(Qt.AlignCenter)

        return label

    # =========================================================
    # Public API
    # =========================================================

    def set_page(self, current: int, total: int):

        self.page_label.setText(
            f"Page: {current} / {total}"
        )

    def set_zoom(self, zoom: int):

        self.zoom_label.setText(
            f"Zoom: {zoom}%"
        )

    def set_word_count(self, words: int):

        self.words_label.setText(
            f"Words: {words:,}"
        )

    def set_progress(self, value: int):

        self.progress.setValue(value)

    def reset_progress(self):

        self.progress.setValue(0)

    def set_status(self, message: str, timeout: int = 0):

        self.showMessage(message, timeout)