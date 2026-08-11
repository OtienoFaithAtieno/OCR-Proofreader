"""Application bootstrap for the Proofreader desktop app."""

import sys

from PySide6.QtWidgets import QApplication

from app.ui.mainwindow import MainWindow


def main() -> int:
    """Create and show the application window."""
    app = QApplication.instance() or QApplication(sys.argv)

    app.setApplicationName("Proofreader")
    app.setOrganizationName("Proofreader")
    app.setApplicationVersion("0.1.0")

    window = MainWindow()
    window.show()

    return app.exec()
