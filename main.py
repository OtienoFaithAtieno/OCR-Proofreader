"""
main.py

Application entry point.
"""

import sys
from PySide6.QtWidgets import QApplication
from app.ui.mainwindow import MainWindow

def main() -> int:
    """Application entry point."""

    app = QApplication(sys.argv)

    # Application information
    app.setApplicationName("Proofreader")
    app.setOrganizationName("Proofreader")
    app.setApplicationVersion("0.1.0")

    # Create main window
    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())