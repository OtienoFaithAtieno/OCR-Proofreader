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

from pathlib import Path

from PySide6.QtCore import Qt, QSettings, QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QFileDialog,
    QInputDialog,
    QMainWindow,
    QMessageBox,
)

from app.cleaner.cleaner import clean_document
from app.cleaner.rules.fonts import normalize_fonts
from app.core.pipeline import process_docx, process_pdf
from app.exporter.exporter import export_document_to_docx
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
        self.menu.action_open_docx.triggered.connect(self.open_docx)

        self.toolbar.action_open.triggered.connect(
            self.open_pdf
        )

        self.menu.action_export_docx.triggered.connect(
            self.export_docx
        )
        self.menu.action_new.triggered.connect(self.new_document)
        self.menu.action_save.triggered.connect(self.export_docx)
        self.menu.action_save_as.triggered.connect(self.export_docx)
        self.menu.action_export.triggered.connect(self.export_docx)
        self.menu.action_export_pdf.triggered.connect(self.export_not_available)
        self.menu.action_export_html.triggered.connect(self.export_not_available)
        self.menu.action_export_markdown.triggered.connect(self.export_not_available)

        #
        # VIEW
        #

        self.menu.action_toggle_theme.triggered.connect(
            self.toggle_theme
        )
        self.menu.action_fullscreen.triggered.connect(self.toggle_fullscreen)
        self.menu.action_zoom_in.triggered.connect(self.zoom_in)
        self.menu.action_zoom_out.triggered.connect(self.zoom_out)
        self.menu.action_reset_zoom.triggered.connect(self.reset_zoom)

        self.menu.action_undo.triggered.connect(self.central.document_panel.editor.undo)
        self.menu.action_redo.triggered.connect(self.central.document_panel.editor.redo)
        self.menu.action_cut.triggered.connect(self.central.document_panel.editor.cut)
        self.menu.action_copy.triggered.connect(self.central.document_panel.editor.copy)
        self.menu.action_paste.triggered.connect(self.central.document_panel.editor.paste)
        self.menu.action_find.triggered.connect(self.find_text)

        self.menu.action_clean_document.triggered.connect(self.clean_current_document)
        self.menu.action_normalize_fonts.triggered.connect(self.normalize_current_fonts)
        self.menu.action_detect_tables.triggered.connect(self.show_tool_message)
        self.menu.action_detect_images.triggered.connect(self.show_tool_message)
        self.menu.action_preferences.triggered.connect(self.show_preferences)
        self.menu.action_documentation.triggered.connect(self.show_documentation)

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
        """Open a PDF, process it, and display the extracted text."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open PDF",
            str(Path.home()),
            "PDF Files (*.pdf)",
        )

        if not file_path:
            return

        self.status.showMessage(f"Loading {Path(file_path).name}...", 3000)

        try:
            result = process_pdf(file_path)
        except Exception as exc:  # pragma: no cover - UI feedback path
            QMessageBox.critical(self, "PDF Error", str(exc))
            return

        self.central.set_document_model(result["document"])

        self.status.set_status(f"Loaded {Path(file_path).name}")
        self.status.set_page(1, result["metadata"]["page_count"])
        self.status.set_word_count(len(result["text"].split()))

    def open_docx(self):
        """Open an unformatted DOCX as editable document content."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Word Document",
            str(Path.home()),
            "Word Documents (*.docx)",
        )
        if not file_path:
            return

        try:
            result = process_docx(file_path)
        except Exception as exc:  # pragma: no cover - UI feedback path
            QMessageBox.critical(self, "DOCX Error", str(exc))
            return

        self.central.set_document_model(result["document"])
        self.central.pdf_panel.set_source_text(result["text"])
        self.status.set_status(f"Opened {Path(file_path).name}")
        self.status.set_page(1, result["metadata"]["page_count"])
        self.status.set_word_count(len(result["text"].split()))

    def toggle_theme(self):
        """
        Toggle dark/light theme.
        """

        self.theme_manager.toggle(self)

    def new_document(self):
        """Clear the current document and return to an empty workspace."""
        self.central.clear()
        self.central.pdf_panel._document = None
        self.central.document_panel._document = None
        self.status.set_status("New document")

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def zoom_in(self):
        self.central.document_panel.editor.zoomIn(1)

    def zoom_out(self):
        self.central.document_panel.editor.zoomOut(1)

    def reset_zoom(self):
        self.central.document_panel.editor.setFontPointSize(11)

    def find_text(self):
        text, accepted = QInputDialog.getText(self, "Find", "Text:")
        if accepted and text:
            self.central.document_panel.editor.find(text)

    def clean_current_document(self):
        if self.central.document_model:
            clean_document(self.central.document_model)
            self.central.document_panel._show_selected_page(
                self.central.document_panel._current_page_index
            )
            self.status.set_status("Formatting cleaned")

    def normalize_current_fonts(self):
        if self.central.document_model:
            normalize_fonts(self.central.document_model)
            self.status.set_status("Fonts normalized")

    def show_tool_message(self):
        self.status.set_status("This tool is not implemented yet")

    def show_preferences(self):
        QMessageBox.information(self, "Preferences", "Preferences are not implemented yet.")

    def export_not_available(self):
        """Explain which export format is currently supported."""
        self.status.set_status("DOCX is the currently supported export format")

    def open_docx_not_available(self):
        """Explain that PDF import is currently the input workflow."""
        self.status.set_status("Open a PDF to create an editable DOCX document")

    def show_documentation(self):
        QMessageBox.information(
            self,
            "Documentation",
            "Open README.md in the project folder for documentation.",
        )

    def export_docx(self):
        """Export the active document using the same flow for PDF or DOCX sources."""
        document_model = self.central.document_model
        if document_model is None:
            document_model = self.central.pdf_panel._document
        if document_model is None:
            QMessageBox.information(
                self,
                "Nothing to Export",
                "Open a PDF or Word document before exporting a DOCX file.",
            )
            return

        default_name = Path(document_model.filename).stem + ".docx"
        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export as DOCX",
            str(Path.home() / default_name),
            "Word Documents (*.docx)",
        )
        if not output_path:
            return

        try:
            export_document_to_docx(document_model, output_path)
        except Exception as exc:  # pragma: no cover - UI feedback path
            QMessageBox.critical(self, "Export Error", str(exc))
            return

        self.status.set_status(f"Exported {Path(output_path).name}")

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