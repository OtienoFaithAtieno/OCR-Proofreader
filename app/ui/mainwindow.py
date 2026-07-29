"""
main_window.py

Main application window for the Proofreading Application.

Responsibilities
----------------
- Create the main window
- Assemble all UI components
- Restore/save window settings
- Connect high-level actions
- Delegate functionality to specialized modules

All UI components (menus, toolbars, docks, themes, etc.)
are implemented in their own modules.
"""

from PySide6.QtCore import Qt, QSettings, QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
)

from app.ui.menubar import MenuBar
from app.ui.toolbar import ToolBar
from app.ui.statusbar import StatusBar
from app.ui.centralwidget import CentralWidget
from app.ui.docmanager import DockManager
from app.ui.theme import ThemeManager


class MainWindow(QMainWindow):
    """
    Main application window.
    """

    ORGANIZATION = "Proofreader"
    APPLICATION = "ProofreaderApp"

    def __init__(self):
        super().__init__()

        self.settings = QSettings(
            self.ORGANIZATION,
            self.APPLICATION
        )

        self.setWindowTitle("Proofreader")
        self.resize(1600, 900)
        self.setMinimumSize(QSize(1200, 700))

        self._create_ui()
        self._connect_signals()
        self._restore_settings()

    # --------------------------------------------------
    # UI Creation
    # --------------------------------------------------

    def _create_ui(self):
        """Create all UI components."""

        # Theme manager
        self.theme_manager = ThemeManager()

        # Central widget
        self.central = CentralWidget(self)
        self.setCentralWidget(self.central)

        # Menu
        self.menu = MenuBar(self)
        self.setMenuBar(self.menu)

        # Toolbar
        self.toolbar = ToolBar(self)
        self.toolbar.setObjectName("main_toolbar")
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        # Status bar
        self.status = StatusBar(self)
        self.setStatusBar(self.status)

        # Dock widgets
        self.docks = DockManager(self)
        self.docks.create_docks()

    # --------------------------------------------------
    # Connections
    # --------------------------------------------------

    def _connect_signals(self):
        """
        Connect actions exposed by MenuBar and ToolBar.

        Assumes menubar.py and toolbar.py expose QAction
        objects as attributes.
        """

        #
        # FILE
        #

        self.menu.action_exit.triggered.connect(self.close)

        self.menu.action_open_pdf.triggered.connect(
            self.open_pdf
        )

        self.toolbar.action_open.triggered.connect(
            self.open_pdf
        )

        #
        # VIEW
        #

        self.menu.action_toggle_theme.triggered.connect(
            self.toggle_theme
        )

        #
        # HELP
        #

        self.menu.action_about.triggered.connect(
            self.show_about
        )

    # --------------------------------------------------
    # Placeholder Slots
    # --------------------------------------------------

    def open_pdf(self):
        """
        Placeholder for PDF loading.
        """

        self.status.showMessage(
            "Open PDF clicked...",
            3000
        )

    def toggle_theme(self):
        """
        Toggle dark/light theme.
        """

        self.theme_manager.toggle(self)

    def show_about(self):
        """
        Display About dialog.
        """

        QMessageBox.about(
            self,
            "About",
            (
                "Proofreader\n\n"
                "OCR & Document Processing Suite\n\n"
                "Version 0.1"
            )
        )

    # --------------------------------------------------
    # Settings
    # --------------------------------------------------

    def _restore_settings(self):
        """Restore window geometry/state."""

        geometry = self.settings.value("geometry")
        state = self.settings.value("windowState")

        if geometry:
            self.restoreGeometry(geometry)

        if state:
            self.restoreState(state)

    def _save_settings(self):
        """Save window geometry/state."""

        self.settings.setValue(
            "geometry",
            self.saveGeometry()
        )

        self.settings.setValue(
            "windowState",
            self.saveState()
        )

    # --------------------------------------------------
    # Events
    # --------------------------------------------------

    def closeEvent(self, event):
        """
        Save settings before exit.
        """

        self._save_settings()

        super().closeEvent(event)